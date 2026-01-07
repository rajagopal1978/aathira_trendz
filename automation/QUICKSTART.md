# Quick Start Guide - Deploy Aathira Trendz to GCP

## Step 1: Prepare Your Environment

### Install Python Dependencies

```bash
cd automation
pip install -r requirements.txt
```

### Verify Credentials File

The GCP credentials file is already in place at:
```
automation/config/gcp-credentials.json
```

**Project ID:** jvl-tech-medai
**Service Account:** vertex-express@jvl-tech-medai.iam.gserviceaccount.com

## Step 2: Review Configuration

Check `config.yaml` settings:

```yaml
instance:
  name: "instance-chem-info-web"    # Your instance name
  machine_type: "e2-medium"          # ~$25-30/month

application:
  github_repo: "https://github.com/rajagopal1978/aathira_trendz.git"
  port: 3000
```

## Step 3: Deploy to GCP

Run the deployment script:

```bash
python deploy.py
```

**What happens:**
- Creates a GCP Compute Engine instance
- Installs Node.js 20, Nginx, PM2
- Clones your GitHub repository
- Builds the Next.js application
- Starts the website with PM2
- Sets up Nginx reverse proxy
- Opens firewall ports (80, 443, 3000)

**Deployment time:** ~5-10 minutes

## Step 4: Access Your Website

After deployment completes, you'll see:

```
==================================================
DEPLOYMENT SUCCESSFUL!
==================================================

Instance Name: instance-chem-info-web
External IP: 34.123.45.67

Access your website at:
  → http://34.123.45.67
  → http://34.123.45.67:3000 (Direct Next.js)
==================================================
```

Open the URL in your browser!

## Additional Commands

### Check Instance Status

```bash
python status.py
```

### Update Website (after pushing to GitHub)

```bash
python update.py
```

Then SSH into instance and run the update commands shown.

### Delete Instance

```bash
python destroy.py
```

## SSH Access

To SSH into your instance:

```bash
gcloud compute ssh instance-chem-info-web --zone=us-central1-a --project=jvl-tech-medai
```

## Monitoring Application

Once SSH'd into the instance:

```bash
# View application status
pm2 status

# View logs
pm2 logs aathira-trendz

# Restart application
pm2 restart aathira-trendz

# Check Nginx
sudo systemctl status nginx
```

## Troubleshooting

### Instance creation fails

- Check GCP billing is enabled
- Verify service account permissions
- Check compute engine quotas in GCP Console

### Website not accessible

1. Wait 5-10 minutes for full initialization
2. Check firewall rules in GCP Console
3. Verify instance is running: `python status.py`
4. Check logs: SSH in and run `pm2 logs`

### Build errors

SSH into instance:

```bash
cd /var/www/aathira-trendz
npm install
npm run build
pm2 restart aathira-trendz
```

## Cost Management

### Estimated Monthly Costs

- **Compute Instance (e2-medium):** ~$25-30
- **Storage (30GB):** ~$2
- **Network:** Variable (usually minimal)

**Total:** ~$27-35/month

### Save Costs

- Stop instance when not needed:
  ```bash
  gcloud compute instances stop instance-chem-info-web --zone=us-central1-a
  ```

- Start instance:
  ```bash
  gcloud compute instances start instance-chem-info-web --zone=us-central1-a
  ```

- Delete completely: `python destroy.py`

## Setting Up Custom Domain (Optional)

1. Get external IP: `python status.py`
2. In your domain DNS settings, create an A record pointing to the IP
3. Update `config.yaml` with your domain
4. Redeploy or configure Nginx manually

## Next Steps

- ✅ Website is live!
- Configure SSL/HTTPS (recommended for production)
- Set up monitoring and alerts
- Configure automated backups
- Add custom domain
- Set up CI/CD pipeline

## Support

- View GCP Console: https://console.cloud.google.com
- Check instance logs in GCP Console → Compute Engine → Instances
- Review serial port output for startup script logs

---

**Happy Deploying! 🚀**
