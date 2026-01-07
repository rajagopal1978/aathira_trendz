#!/usr/bin/env python3
"""
Deploy Aathira Trendz to existing GCP instance
"""

import yaml
import logging
import time
import subprocess
from google.cloud import compute_v1
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def get_instance_ip(config):
    """Get the external IP of the existing instance"""
    credentials = service_account.Credentials.from_service_account_file(
        config['gcp']['credentials_path'],
        scopes=['https://www.googleapis.com/auth/compute', 'https://www.googleapis.com/auth/cloud-platform']
    )

    client = compute_v1.InstancesClient(credentials=credentials)

    instance = client.get(
        project=config['gcp']['project_id'],
        zone=config['gcp']['zone'],
        instance=config['instance']['name']
    )

    if instance.network_interfaces:
        access_configs = instance.network_interfaces[0].access_configs
        if access_configs:
            return access_configs[0].nat_i_p
    return None


def deploy_to_existing():
    """Deploy to existing instance using gcloud SSH"""
    config = load_config()

    logger.info("=" * 60)
    logger.info("Deploying to Existing Instance")
    logger.info("=" * 60)

    project_id = config['gcp']['project_id']
    zone = config['gcp']['zone']
    instance_name = config['instance']['name']
    app_name = config['application']['name']
    github_repo = config['application']['github_repo']
    branch = config['application']['branch']
    port = config['application']['port']

    logger.info(f"\nTarget Instance: {instance_name}")
    logger.info(f"Project: {project_id}")
    logger.info(f"Zone: {zone}")

    # Get IP
    external_ip = get_instance_ip(config)
    if external_ip:
        logger.info(f"External IP: {external_ip}")

    # Deployment commands
    deployment_script = f"""
#!/bin/bash
set -e

echo "=========================================="
echo "Deploying Aathira Trendz"
echo "=========================================="

# Update system
echo "[1/8] Updating system..."
sudo apt-get update

# Install Node.js if not present
if ! command -v node &> /dev/null; then
    echo "[2/8] Installing Node.js 20..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
    sudo apt-get install -y nodejs
else
    echo "[2/8] Node.js already installed ($(node -v))"
fi

# Install dependencies
echo "[3/8] Installing required packages..."
sudo apt-get install -y build-essential git nginx

# Setup firewall
echo "[4/8] Configuring firewall..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow {port}
sudo ufw --force enable

# Stop existing app if running
echo "[5/8] Stopping existing application..."
if command -v pm2 &> /dev/null; then
    pm2 stop {app_name} || true
    pm2 delete {app_name} || true
fi

# Clone or update repository
echo "[6/8] Setting up application..."
if [ -d "/var/www/{app_name}" ]; then
    echo "Directory exists, pulling latest changes..."
    cd /var/www/{app_name}
    sudo git pull origin {branch} || sudo git reset --hard && sudo git pull origin {branch}
else
    echo "Cloning repository..."
    sudo mkdir -p /var/www/{app_name}
    sudo git clone {github_repo} /var/www/{app_name}
    cd /var/www/{app_name}
fi

# Set permissions
sudo chown -R $USER:$USER /var/www/{app_name}

# Install dependencies and build
echo "[7/8] Installing dependencies and building..."
cd /var/www/{app_name}
npm install
npm run build

# Install PM2 if not present
if ! command -v pm2 &> /dev/null; then
    echo "Installing PM2..."
    sudo npm install -g pm2
fi

# Start application
echo "[8/8] Starting application..."
pm2 start npm --name "{app_name}" -- start
pm2 startup systemd -u $USER --hp $HOME
pm2 save

# Configure Nginx
echo "Configuring Nginx..."
sudo bash -c 'cat > /etc/nginx/sites-available/{app_name} << '"'"'EOF'"'"'
server {{
    listen 80;
    server_name _;

    location / {{
        proxy_pass http://localhost:{port};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\$http_upgrade;
        proxy_set_header Connection '"'"'upgrade'"'"';
        proxy_set_header Host \\$host;
        proxy_cache_bypass \\$http_upgrade;
        proxy_set_header X-Real-IP \\$remote_addr;
        proxy_set_header X-Forwarded-For \\$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \\$scheme;
    }}
}}
EOF'

sudo ln -sf /etc/nginx/sites-available/{app_name} /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
pm2 status
"""

    # Save script to temp file
    import tempfile
    import os

    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, 'deploy_aathira.sh')

    with open(script_path, 'w') as f:
        f.write(deployment_script)

    logger.info("\n" + "=" * 60)
    logger.info("Executing deployment on instance...")
    logger.info("=" * 60)

    # Copy script to instance
    logger.info("\nStep 1: Copying deployment script...")
    copy_cmd = [
        'gcloud', 'compute', 'scp',
        script_path,
        f'{instance_name}:/tmp/deploy_aathira.sh',
        f'--project={project_id}',
        f'--zone={zone}'
    ]

    try:
        result = subprocess.run(copy_cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            logger.info("✓ Script copied successfully")
        else:
            logger.error(f"Failed to copy script: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error copying script: {e}")
        return False

    # Execute script on instance
    logger.info("\nStep 2: Executing deployment script...")
    logger.info("(This may take 5-10 minutes...)\n")

    exec_cmd = [
        'gcloud', 'compute', 'ssh',
        instance_name,
        f'--project={project_id}',
        f'--zone={zone}',
        '--command', 'bash /tmp/deploy_aathira.sh'
    ]

    try:
        result = subprocess.run(exec_cmd, text=True, timeout=600)

        if result.returncode == 0:
            logger.info("\n" + "=" * 60)
            logger.info("✓ DEPLOYMENT SUCCESSFUL!")
            logger.info("=" * 60)
            logger.info(f"\nYour website is now live at:")
            logger.info(f"  → http://{external_ip}")
            logger.info(f"  → http://{external_ip}:{port}")
            logger.info("\n" + "=" * 60)
            return True
        else:
            logger.error("Deployment script failed")
            return False

    except subprocess.TimeoutExpired:
        logger.warning("\nDeployment is taking longer than expected.")
        logger.info("You can check status with: python status.py")
        return False
    except Exception as e:
        logger.error(f"Error executing deployment: {e}")
        return False


if __name__ == "__main__":
    try:
        success = deploy_to_existing()
        exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Deployment failed: {e}", exc_info=True)
        exit(1)
