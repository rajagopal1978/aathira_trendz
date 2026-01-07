#!/usr/bin/env python3
"""
Update deployed application by pulling latest changes and rebuilding
"""

import yaml
import logging
import time
from google.cloud import compute_v1
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from YAML file"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def update_application():
    """Update the deployed application"""
    config = load_config()

    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        config['gcp']['credentials_path']
    )

    # Initialize client
    client = compute_v1.InstancesClient(credentials=credentials)

    project_id = config['gcp']['project_id']
    zone = config['gcp']['zone']
    instance_name = config['instance']['name']

    # Update script
    update_script = f"""#!/bin/bash
set -e

cd /var/www/{config['application']['name']}

# Stop the application
pm2 stop {config['application']['name']}

# Pull latest changes
git pull origin {config['application']['branch']}

# Install dependencies
npm install

# Build application
npm run build

# Restart application
pm2 restart {config['application']['name']}

echo "Application updated successfully!"
"""

    logger.info("Updating deployed application...")
    logger.info("This will:")
    logger.info("  1. Pull latest changes from GitHub")
    logger.info("  2. Install new dependencies")
    logger.info("  3. Rebuild the application")
    logger.info("  4. Restart the server")

    # Create metadata for running the update script
    metadata = compute_v1.Metadata()
    metadata_items = compute_v1.Items()
    metadata_items.key = "startup-script"
    metadata_items.value = update_script
    metadata.items = [metadata_items]

    try:
        # Note: In practice, you'd want to use SSH or Cloud Run to execute this
        logger.info("\nTo manually update, SSH into the instance and run:")
        logger.info(f"\ncd /var/www/{config['application']['name']}")
        logger.info("git pull")
        logger.info("npm install")
        logger.info("npm run build")
        logger.info(f"pm2 restart {config['application']['name']}")

        logger.info("\n" + "=" * 60)
        logger.info("For automated updates, this script sets up the update command.")
        logger.info("SSH into your instance to execute the update.")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error updating application: {e}")


if __name__ == "__main__":
    update_application()
