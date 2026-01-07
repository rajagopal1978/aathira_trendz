#!/usr/bin/env python3
"""
Automated Deployment Script for Aathira Trendz Website
Deploys Next.js application to Google Cloud Compute Engine
"""

import os
import sys
import time
import yaml
import logging
from pathlib import Path
from google.cloud import compute_v1
from google.oauth2 import service_account
import paramiko

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GCPDeployment:
    """Handles deployment to Google Cloud Platform"""

    def __init__(self, config_path='config.yaml'):
        """Initialize GCP deployment with configuration"""
        self.config = self.load_config(config_path)
        self.credentials = self.load_credentials()
        self.compute_client = compute_v1.InstancesClient(credentials=self.credentials)
        self.firewall_client = compute_v1.FirewallsClient(credentials=self.credentials)

    def load_config(self, config_path):
        """Load configuration from YAML file"""
        logger.info(f"Loading configuration from {config_path}")
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def load_credentials(self):
        """Load GCP service account credentials"""
        creds_path = self.config['gcp']['credentials_path']
        logger.info(f"Loading GCP credentials from {creds_path}")
        return service_account.Credentials.from_service_account_file(creds_path)

    def create_instance(self):
        """Create a new Compute Engine instance"""
        project_id = self.config['gcp']['project_id']
        zone = self.config['gcp']['zone']
        instance_name = self.config['instance']['name']

        logger.info(f"Creating instance {instance_name} in {zone}")

        # Define instance configuration
        machine_type = f"zones/{zone}/machineTypes/{self.config['instance']['machine_type']}"

        instance = compute_v1.Instance()
        instance.name = instance_name
        instance.machine_type = machine_type

        # Boot disk configuration
        boot_disk = compute_v1.AttachedDisk()
        initialize_params = compute_v1.AttachedDiskInitializeParams()
        initialize_params.source_image = (
            f"projects/{self.config['instance']['image_project']}/global/images/family/"
            f"{self.config['instance']['image_family']}"
        )
        initialize_params.disk_size_gb = self.config['instance']['boot_disk_size']
        initialize_params.disk_type = f"zones/{zone}/diskTypes/{self.config['instance']['boot_disk_type']}"

        boot_disk.initialize_params = initialize_params
        boot_disk.auto_delete = True
        boot_disk.boot = True
        instance.disks = [boot_disk]

        # Network configuration
        network_interface = compute_v1.NetworkInterface()
        network_interface.name = "global/networks/default"

        # Access configuration for external IP
        access_config = compute_v1.AccessConfig()
        access_config.name = "External NAT"
        access_config.type_ = "ONE_TO_ONE_NAT"
        network_interface.access_configs = [access_config]

        instance.network_interfaces = [network_interface]

        # Metadata for startup script
        metadata = compute_v1.Metadata()
        metadata_items = compute_v1.Items()
        metadata_items.key = "startup-script"
        metadata_items.value = self.generate_startup_script()
        metadata.items = [metadata_items]
        instance.metadata = metadata

        # Create the instance
        request = compute_v1.InsertInstanceRequest()
        request.project = project_id
        request.zone = zone
        request.instance_resource = instance

        try:
            operation = self.compute_client.insert(request=request)
            logger.info(f"Instance creation initiated. Waiting for completion...")
            self.wait_for_operation(operation, zone)
            logger.info(f"Instance {instance_name} created successfully!")
            return True
        except Exception as e:
            logger.error(f"Error creating instance: {e}")
            return False

    def generate_startup_script(self):
        """Generate startup script for instance initialization"""
        script = f"""#!/bin/bash
set -e

# Update system
apt-get update
apt-get upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_{self.config['deployment']['nodejs_version']} | bash -
apt-get install -y nodejs

# Install build essentials
apt-get install -y build-essential git

# Install Nginx
apt-get install -y nginx

# Configure firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow {self.config['application']['port']}
ufw --force enable

# Create application directory
mkdir -p /var/www/{self.config['application']['name']}
cd /var/www/{self.config['application']['name']}

# Clone repository
git clone {self.config['application']['github_repo']} .
git checkout {self.config['application']['branch']}

# Install dependencies
npm install

# Build application
npm run build

# Install PM2 for process management
npm install -g pm2

# Start application with PM2
pm2 start npm --name "{self.config['application']['name']}" -- start
pm2 startup systemd
pm2 save

# Configure Nginx
cat > /etc/nginx/sites-available/{self.config['application']['name']} << 'EOF'
server {{
    listen 80;
    server_name _;

    location / {{
        proxy_pass http://localhost:{self.config['application']['port']};
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }}
}}
EOF

ln -sf /etc/nginx/sites-available/{self.config['application']['name']} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo "Deployment completed successfully!"
"""
        return script

    def setup_firewall_rules(self):
        """Create firewall rules for the application"""
        project_id = self.config['gcp']['project_id']

        for rule in self.config['firewall']:
            logger.info(f"Creating firewall rule: {rule['name']}")

            firewall_rule = compute_v1.Firewall()
            firewall_rule.name = f"{self.config['application']['name']}-{rule['name']}"
            firewall_rule.direction = "INGRESS"
            firewall_rule.priority = 1000

            allowed = compute_v1.Allowed()
            allowed.I_p_protocol = rule['protocol']
            allowed.ports = [str(rule['port'])]
            firewall_rule.allowed = [allowed]

            firewall_rule.source_ranges = ["0.0.0.0/0"]
            firewall_rule.target_tags = [self.config['instance']['name']]

            request = compute_v1.InsertFirewallRequest()
            request.project = project_id
            request.firewall_resource = firewall_rule

            try:
                self.firewall_client.insert(request=request)
                logger.info(f"Firewall rule {rule['name']} created successfully")
            except Exception as e:
                logger.warning(f"Firewall rule might already exist: {e}")

    def wait_for_operation(self, operation, zone):
        """Wait for a GCP operation to complete"""
        project_id = self.config['gcp']['project_id']

        while operation.status != compute_v1.Operation.Status.DONE:
            time.sleep(5)
            operation = self.compute_client.get(
                project=project_id,
                zone=zone,
                instance=self.config['instance']['name']
            )

    def get_instance_ip(self):
        """Get the external IP address of the instance"""
        project_id = self.config['gcp']['project_id']
        zone = self.config['gcp']['zone']
        instance_name = self.config['instance']['name']

        try:
            instance = self.compute_client.get(
                project=project_id,
                zone=zone,
                instance=instance_name
            )

            if instance.network_interfaces:
                access_configs = instance.network_interfaces[0].access_configs
                if access_configs:
                    return access_configs[0].nat_i_p
        except Exception as e:
            logger.error(f"Error getting instance IP: {e}")

        return None

    def deploy(self):
        """Main deployment workflow"""
        logger.info("=" * 60)
        logger.info("Starting Aathira Trendz Deployment")
        logger.info("=" * 60)

        # Step 1: Setup firewall rules
        logger.info("\nStep 1: Setting up firewall rules...")
        self.setup_firewall_rules()

        # Step 2: Create instance
        logger.info("\nStep 2: Creating Compute Engine instance...")
        if not self.create_instance():
            logger.error("Deployment failed!")
            return False

        # Step 3: Wait for instance to be ready
        logger.info("\nStep 3: Waiting for instance initialization...")
        time.sleep(60)  # Wait for startup script to begin

        # Step 4: Get instance IP
        logger.info("\nStep 4: Retrieving instance IP address...")
        external_ip = self.get_instance_ip()

        if external_ip:
            logger.info("\n" + "=" * 60)
            logger.info("DEPLOYMENT SUCCESSFUL!")
            logger.info("=" * 60)
            logger.info(f"\nInstance Name: {self.config['instance']['name']}")
            logger.info(f"External IP: {external_ip}")
            logger.info(f"\nAccess your website at:")
            logger.info(f"  → http://{external_ip}")
            logger.info(f"  → http://{external_ip}:3000 (Direct Next.js)")
            logger.info("\nNote: It may take 5-10 minutes for the application to be fully ready.")
            logger.info("=" * 60)
        else:
            logger.warning("Could not retrieve instance IP. Check GCP Console.")

        return True


def main():
    """Main entry point"""
    try:
        # Change to script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)

        # Run deployment
        deployer = GCPDeployment()
        success = deployer.deploy()

        sys.exit(0 if success else 1)

    except Exception as e:
        logger.error(f"Deployment failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
