# Aathira Trendz - Automated GCP Deployment

This directory contains Python automation scripts to deploy the Aathira Trendz website to Google Cloud Platform.

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with billing enabled
- Service account credentials with necessary permissions
- Git installed locally

## Setup

### 1. Install Python Dependencies

```bash
cd automation
pip install -r requirements.txt
```

### 2. Configure Deployment

Edit `config.yaml` to customize your deployment:

- **GCP Settings**: Project ID, region, zone
- **Instance Configuration**: Machine type, disk size, OS image
- **Application Settings**: GitHub repo, port, branch
- **Firewall Rules**: Ports to open

### 3. Verify Credentials

Ensure `config/gcp-credentials.json` contains your valid service account credentials.

## Usage

### Deploy to GCP

Run the main deployment script:

```bash
python deploy.py
```

This will:
1. Create firewall rules
2. Provision a Compute Engine instance
3. Install Node.js and required dependencies
4. Clone the GitHub repository
5. Build and start the Next.js application
6. Configure Nginx as reverse proxy
7. Display the external IP address

### Check Instance Status

```bash
python status.py
```

### Update Deployed Application

```bash
python update.py
```

### Destroy Instance

```bash
python destroy.py
```

## Deployment Workflow

The automated deployment performs these steps:

1. **Firewall Configuration**
   - Opens ports 80 (HTTP), 443 (HTTPS), and 3000 (Next.js)

2. **Instance Creation**
   - Creates Ubuntu 22.04 LTS instance
   - Configures external IP address

3. **Software Installation**
   - Node.js 20.x
   - Nginx web server
   - PM2 process manager
   - Git

4. **Application Deployment**
   - Clones repository from GitHub
   - Installs npm dependencies
   - Builds production Next.js application
   - Starts app with PM2

5. **Nginx Configuration**
   - Reverse proxy setup
   - Routes HTTP traffic to Next.js app

## Configuration Files

- **config.yaml**: Main configuration file
- **config/gcp-credentials.json**: GCP service account credentials
- **requirements.txt**: Python dependencies

## Accessing Your Website

After successful deployment, access your website at:

- `http://[EXTERNAL_IP]` - Through Nginx proxy
- `http://[EXTERNAL_IP]:3000` - Direct Next.js server

## Monitoring

The application runs under PM2 process manager. SSH into your instance and use:

```bash
# Check application status
pm2 status

# View logs
pm2 logs aathira-trendz

# Restart application
pm2 restart aathira-trendz
```

## Troubleshooting

### Deployment Fails

1. Check GCP credentials are valid
2. Verify project ID and permissions
3. Ensure billing is enabled
4. Check quotas for Compute Engine

### Website Not Accessible

1. Verify firewall rules are created
2. Check instance is running: `python status.py`
3. SSH into instance and check logs: `pm2 logs`
4. Verify Nginx is running: `sudo systemctl status nginx`

### Build Errors

SSH into the instance and check:

```bash
cd /var/www/aathira-trendz
npm run build
```

## Security Notes

- **Never commit** `gcp-credentials.json` to public repositories
- The credentials file is in `.gitignore`
- Use least-privilege service account permissions
- Enable firewall rules only for required ports
- Consider setting up HTTPS with SSL certificates

## Cost Estimation

Running costs (approximate):

- **e2-medium instance**: ~$25-30/month
- **Storage (30GB)**: ~$2/month
- **Network egress**: Variable based on traffic

Stop or delete instances when not needed to reduce costs.

## Support

For issues or questions:
- Check GCP Console for detailed logs
- Review instance serial port output
- Contact your GCP administrator

## License

This automation script is part of the Aathira Trendz project.
