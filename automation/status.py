#!/usr/bin/env python3
"""
Check status of deployed Aathira Trendz instance
"""

import yaml
import logging
from google.cloud import compute_v1
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from YAML file"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def check_instance_status():
    """Check instance status and display information"""
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

    try:
        # Get instance details
        instance = client.get(
            project=project_id,
            zone=zone,
            instance=instance_name
        )

        # Display information
        logger.info("=" * 60)
        logger.info("INSTANCE STATUS")
        logger.info("=" * 60)
        logger.info(f"Name: {instance.name}")
        logger.info(f"Status: {instance.status}")
        logger.info(f"Machine Type: {instance.machine_type.split('/')[-1]}")
        logger.info(f"Zone: {zone}")

        # Get external IP
        if instance.network_interfaces:
            access_configs = instance.network_interfaces[0].access_configs
            if access_configs:
                external_ip = access_configs[0].nat_i_p
                logger.info(f"External IP: {external_ip}")
                logger.info(f"\nWebsite URLs:")
                logger.info(f"  → http://{external_ip}")
                logger.info(f"  → http://{external_ip}:3000")

        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error retrieving instance status: {e}")
        logger.info("\nInstance may not exist. Run deploy.py to create it.")


if __name__ == "__main__":
    check_instance_status()
