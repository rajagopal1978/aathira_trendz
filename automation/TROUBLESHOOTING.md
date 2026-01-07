# Troubleshooting GCP Deployment

## Current Issue: Authentication Error (401)

### Problem
The service account `vertex-express@jvl-tech-medai.iam.gserviceaccount.com` doesn't have the required permissions for Compute Engine operations.

### Error Message
```
401 POST https://compute.googleapis.com/compute/v1/projects/jvl-tech-medai/...
Request had invalid authentication credentials.
```

## Solution Options

### Option 1: Add Required Permissions to Service Account (Recommended)

You need to grant the following IAM roles to the service account in GCP Console:

1. Go to [GCP IAM & Admin Console](https://console.cloud.google.com/iam-admin/iam?project=jvl-tech-medai)

2. Find the service account: `vertex-express@jvl-tech-medai.iam.gserviceaccount.com`

3. Click "Edit" (pencil icon)

4. Add these roles:
   - **Compute Admin** (`roles/compute.admin`) - Full control of Compute Engine resources
   - OR **Compute Instance Admin** (`roles/compute.instanceAdmin.v1`) - Create and manage instances
   - **Service Account User** (`roles/iam.serviceAccountUser`) - Required for instance creation

5. Click "Save"

6. Wait 1-2 minutes for permissions to propagate

7. Run the deployment again:
   ```bash
   cd automation
   python deploy.py
   ```

### Option 2: Create a New Service Account

If you don't have permission to modify the existing service account:

1. Go to [Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?project=jvl-tech-medai)

2. Click "CREATE SERVICE ACCOUNT"

3. Fill in details:
   - **Name**: `compute-deployment`
   - **Description**: Service account for deploying web applications

4. Click "CREATE AND CONTINUE"

5. Grant roles:
   - Compute Admin
   - Service Account User

6. Click "CONTINUE" then "DONE"

7. Click on the new service account

8. Go to "KEYS" tab

9. Click "ADD KEY" → "Create new key"

10. Choose "JSON" and click "CREATE"

11. Download the JSON file

12. Replace the credentials file:
    ```bash
    # Save the new JSON file as:
    automation/config/gcp-credentials.json
    ```

13. Run deployment again

### Option 3: Use gcloud CLI Authentication

If you have gcloud CLI installed and authenticated:

1. Authenticate:
   ```bash
   gcloud auth login
   gcloud config set project jvl-tech-medai
   ```

2. Use Application Default Credentials:
   ```bash
   gcloud auth application-default login
   ```

3. Modify `deploy.py` line 52-56 to use default credentials:
   ```python
   def load_credentials(self):
       from google.auth import default
       credentials, project = default()
       return credentials
   ```

4. Run deployment

### Option 4: Manual Deployment via GCP Console

If you can't modify service account permissions, deploy manually:

1. Go to [Compute Engine → VM instances](https://console.cloud.google.com/compute/instances?project=jvl-tech-medai)

2. Click "CREATE INSTANCE"

3. Configure:
   - **Name**: `instance-chem-info-web`
   - **Region**: `us-central1`
   - **Zone**: `us-central1-a`
   - **Machine type**: `e2-medium`
   - **Boot disk**: Ubuntu 22.04 LTS, 30GB

4. Under "Firewall", check:
   - Allow HTTP traffic
   - Allow HTTPS traffic

5. Click "Management" tab → "Automation"

6. In "Startup script", paste:
   ```bash
   #!/bin/bash
   set -e

   # Update system
   apt-get update
   apt-get upgrade -y

   # Install Node.js 20
   curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
   apt-get install -y nodejs

   # Install dependencies
   apt-get install -y build-essential git nginx

   # Setup firewall
   ufw allow 22
   ufw allow 80
   ufw allow 443
   ufw allow 3000
   ufw --force enable

   # Clone and deploy
   mkdir -p /var/www/aathira-trendz
   cd /var/www/aathira-trendz
   git clone https://github.com/rajagopal1978/aathira_trendz.git .
   npm install
   npm run build

   # Install PM2 and start app
   npm install -g pm2
   pm2 start npm --name "aathira-trendz" -- start
   pm2 startup systemd
   pm2 save

   # Configure Nginx
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
       }
   }
   EOF

   ln -sf /etc/nginx/sites-available/aathira-trendz /etc/nginx/sites-enabled/
   rm -f /etc/nginx/sites-enabled/default
   nginx -t && systemctl restart nginx
   ```

7. Click "CREATE"

8. Wait 5-10 minutes for initialization

9. Get the External IP from the instances list

10. Access: `http://[EXTERNAL_IP]`

## Verifying Permissions

To check what permissions the service account has:

```bash
gcloud projects get-iam-policy jvl-tech-medai \
  --flatten="bindings[].members" \
  --filter="bindings.members:vertex-express@jvl-tech-medai.iam.gserviceaccount.com" \
  --format="table(bindings.role)"
```

## Common Permission Issues

### Error: "403 Forbidden"
- Service account lacks permissions
- Solution: Add required IAM roles

### Error: "401 Unauthorized"
- Credentials are invalid or missing scopes
- Solution: Regenerate credentials or add permissions

### Error: "Quota exceeded"
- Project has reached resource limits
- Solution: Request quota increase or delete unused resources

## Getting Help

1. Check GCP Console for detailed error logs
2. Review Compute Engine quotas
3. Verify billing is enabled
4. Check organization policies don't block Compute Engine

## Quick Permission Check

Run this to verify the service account exists:

```bash
gcloud iam service-accounts describe vertex-express@jvl-tech-medai.iam.gserviceaccount.com
```

## Need More Help?

Contact your GCP project administrator to grant the necessary permissions.
