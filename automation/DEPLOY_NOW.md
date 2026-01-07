# Deploy Aathira Trendz to Existing Instance

Your instance is running at:
- **Name**: instance-chem-info-web
- **Zone**: us-central1-f
- **External IP**: 34.134.247.88

## Quick Deploy (Single Command)

Run this command to deploy the website:

```bash
gcloud compute ssh instance-chem-info-web --zone=us-central1-f --project=jvl-tech-medai --command="
sudo apt-get update && \
sudo apt-get install -y curl git build-essential nginx && \
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash - && \
sudo apt-get install -y nodejs && \
sudo mkdir -p /var/www/aathira-trendz && \
cd /var/www/aathira-trendz && \
if [ -d .git ]; then sudo git pull origin main; else sudo git clone https://github.com/rajagopal1978/aathira_trendz.git .; fi && \
sudo chown -R \$USER:\$USER /var/www/aathira-trendz && \
npm install && \
npm run build && \
sudo npm install -g pm2 && \
pm2 stop aathira-trendz || true && \
pm2 delete aathira-trendz || true && \
pm2 start npm --name aathira-trendz -- start && \
pm2 startup systemd && \
pm2 save && \
sudo bash -c 'cat > /etc/nginx/sites-available/aathira-trendz << EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \\\$http_upgrade;
        proxy_set_header Connection upgrade;
        proxy_set_header Host \\\$host;
        proxy_cache_bypass \\\$http_upgrade;
    }
}
EOF' && \
sudo ln -sf /etc/nginx/sites-available/aathira-trendz /etc/nginx/sites-enabled/ && \
sudo rm -f /etc/nginx/sites-enabled/default && \
sudo nginx -t && sudo systemctl restart nginx && \
echo '========================================' && \
echo 'DEPLOYMENT COMPLETE!' && \
echo '========================================' && \
echo 'Website: http://34.134.247.88' && \
echo '========================================'
"
```

## Accessing Your Website

After deployment completes (~5-10 minutes):

→ **http://34.134.247.88**

## Manual Step-by-Step (Alternative)

If the single command doesn't work, SSH in and run commands manually:

### 1. SSH into instance

```bash
gcloud compute ssh instance-chem-info-web --zone=us-central1-f --project=jvl-tech-medai
```

### 2. Run deployment commands

```bash
# Update system
sudo apt-get update
sudo apt-get install -y curl git build-essential nginx

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt-get install -y nodejs

# Clone repository
sudo mkdir -p /var/www/aathira-trendz
cd /var/www/aathira-trendz

# If directory exists, pull latest; otherwise clone
if [ -d .git ]; then
    sudo git pull origin main
else
    sudo git clone https://github.com/rajagopal1978/aathira_trendz.git .
fi

# Set permissions
sudo chown -R $USER:$USER /var/www/aathira-trendz

# Install dependencies and build
npm install
npm run build

# Install PM2
sudo npm install -g pm2

# Stop existing app if running
pm2 stop aathira-trendz || true
pm2 delete aathira-trendz || true

# Start application
pm2 start npm --name "aathira-trendz" -- start
pm2 startup systemd
pm2 save

# Configure Nginx
sudo bash -c 'cat > /etc/nginx/sites-available/aathira-trendz << EOF
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF'

sudo ln -sf /etc/nginx/sites-available/aathira-trendz /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

echo "Deployment complete!"
pm2 status
```

## Check Deployment Status

```bash
# Check if app is running
pm2 status

# View logs
pm2 logs aathira-trendz

# Check Nginx
sudo systemctl status nginx
```

## Update Website Later

```bash
# SSH into instance
gcloud compute ssh instance-chem-info-web --zone=us-central1-f --project=jvl-tech-medai

# Update code
cd /var/www/aathira-trendz
git pull origin main
npm install
npm run build
pm2 restart aathira-trendz
```

## Your Website

**Live at**: http://34.134.247.88

🚀 **Ready to deploy!**
