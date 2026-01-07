# Manual Deployment Guide - Aathira Trendz to GCP

Since the service account credentials are having authentication issues, here's a step-by-step manual deployment guide that will work immediately.

## Quick Deploy (Copy & Paste Method)

### Step 1: Create VM Instance

1. Go to [Google Cloud Console - Create Instance](https://console.cloud.google.com/compute/instancesAdd?project=jvl-tech-medai)

2. Configure the instance:
   ```
   Name: instance-chem-info-web
   Region: us-central1
   Zone: us-central1-a
   Machine type: e2-medium (2 vCPU, 4 GB memory)
   ```

3. **Boot disk**: Click "CHANGE"
   - Operating System: Ubuntu
   - Version: Ubuntu 22.04 LTS
   - Boot disk type: Standard persistent disk
   - Size: 30 GB
   - Click "SELECT"

4. **Firewall**: Check both boxes:
   - ☑ Allow HTTP traffic
   - ☑ Allow HTTPS traffic

5. Expand "**Advanced options**" → "**Management**"

6. In the "**Automation**" section, under "**Startup script**", paste this entire script:

```bash
#!/bin/bash
set -e

echo "=========================================="
echo "Starting Aathira Trendz Deployment"
echo "=========================================="

# Update system
echo "[1/8] Updating system..."
apt-get update
apt-get upgrade -y

# Install Node.js 20
echo "[2/8] Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs

# Install dependencies
echo "[3/8] Installing build tools..."
apt-get install -y build-essential git nginx

# Setup firewall
echo "[4/8] Configuring firewall..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw allow 3000
ufw --force enable

# Clone repository
echo "[5/8] Cloning repository..."
mkdir -p /var/www/aathira-trendz
cd /var/www/aathira-trendz
git clone https://github.com/rajagopal1978/aathira_trendz.git .

# Install npm dependencies
echo "[6/8] Installing npm packages (this may take a few minutes)..."
npm install

# Build application
echo "[7/8] Building Next.js application..."
npm run build

# Install PM2 and start app
echo "[8/8] Starting application with PM2..."
npm install -g pm2
pm2 start npm --name "aathira-trendz" -- start
pm2 startup systemd
pm2 save

# Configure Nginx
echo "Configuring Nginx reverse proxy..."
cat > /etc/nginx/sites-available/aathira-trendz << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/aathira-trendz /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Website is running on port 80"
echo "Access at: http://$(curl -s ifconfig.me)"
echo "=========================================="
```

7. Click "**CREATE**"

### Step 2: Wait for Deployment

- **Instance creation**: ~30 seconds
- **Startup script execution**: ~8-10 minutes
- Total time: **~10 minutes**

### Step 3: Get Your Website URL

1. Go to [Compute Engine - VM Instances](https://console.cloud.google.com/compute/instances?project=jvl-tech-medai)

2. Find your instance: `instance-chem-info-web`

3. Copy the **External IP** address (e.g., 34.123.45.67)

4. Open in browser: `http://[YOUR-EXTERNAL-IP]`

### Step 4: Verify Deployment

Monitor the startup script progress:

1. Click on your instance name: `instance-chem-info-web`

2. Scroll down to "**Logs**" section

3. Click "**Serial port 1 (console)**"

4. Watch for "Deployment Complete!" message

## Troubleshooting

### Website shows "502 Bad Gateway"

The startup script is still running. Wait 5 more minutes.

### Can't access website

1. Check firewall rules allow HTTP:
   ```bash
   gcloud compute firewall-rules list --project=jvl-tech-medai
   ```

2. SSH into instance and check status:
   ```bash
   gcloud compute ssh instance-chem-info-web --zone=us-central1-a
   ```

   Then check:
   ```bash
   # Check if app is running
   pm2 status

   # View app logs
   pm2 logs aathira-trendz

   # Check Nginx
   sudo systemctl status nginx

   # View Nginx logs
   sudo tail -f /var/log/nginx/error.log
   ```

### Build failed

SSH in and rebuild manually:

```bash
cd /var/www/aathira-trendz
npm install
npm run build
pm2 restart aathira-trendz
```

## Post-Deployment

### Access via SSH

```bash
gcloud compute ssh instance-chem-info-web --zone=us-central1-a --project=jvl-tech-medai
```

### Update Website

After pushing changes to GitHub:

```bash
# SSH into instance
gcloud compute ssh instance-chem-info-web --zone=us-central1-a

# Pull latest changes
cd /var/www/aathira-trendz
git pull origin main
npm install
npm run build
pm2 restart aathira-trendz
```

### Monitor Application

```bash
pm2 status              # Check app status
pm2 logs aathira-trendz # View real-time logs
pm2 restart aathira-trendz # Restart app
```

### Stop Instance (Save Costs)

```bash
gcloud compute instances stop instance-chem-info-web --zone=us-central1-a
```

### Start Instance

```bash
gcloud compute instances start instance-chem-info-web --zone=us-central1-a
```

### Delete Instance

```bash
gcloud compute instances delete instance-chem-info-web --zone=us-central1-a
```

Or via Console:
1. Go to VM instances
2. Check the box next to `instance-chem-info-web`
3. Click "DELETE"

## Expected Costs

- **Running 24/7**: ~$27-35/month
- **Stopped instance**: ~$2/month (storage only)
- **Deleted**: $0

## Setup Custom Domain (Optional)

1. Get the External IP from GCP Console

2. In your domain registrar (GoDaddy, Namecheap, etc.):
   - Create an A record
   - Point to your External IP
   - Wait for DNS propagation (5-60 minutes)

3. Update Nginx config:
   ```bash
   sudo nano /etc/nginx/sites-available/aathira-trendz
   ```

   Change `server_name _;` to `server_name yourdomain.com www.yourdomain.com;`

4. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

## Setup SSL/HTTPS (Recommended)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate (replace yourdomain.com)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
```

## Support

- [GCP Documentation](https://cloud.google.com/compute/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [PM2 Documentation](https://pm2.keymetrics.io/)

---

**That's it! Your website will be live in ~10 minutes!** 🚀
