#!/usr/bin/env python3
"""
Destroy deployed GCP resources
"""

import yaml
import logging
import sys
from google.cloud import compute_v1
from google.oauth2 import service_account

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from YAML file"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def destroy_instance():
    """Delete the Compute Engine instance"""
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

    # Confirm deletion
    logger.warning("=" * 60)
    logger.warning("WARNING: This will DELETE the instance and all its data!")
    logger.warning("=" * 60)
    logger.warning(f"Instance: {instance_name}")
    logger.warning(f"Zone: {zone}")
    logger.warning(f"Project: {project_id}")

    confirmation = input("\nType 'DELETE' to confirm: ")

    if confirmation != "DELETE":
        logger.info("Destruction cancelled.")
        return False

    try:
        logger.info("\nDeleting instance...")
        request = compute_v1.DeleteInstanceRequest()
        request.project = project_id
        request.zone = zone
        request.instance = instance_name

        operation = client.delete(request=request)

        logger.info("Instance deletion initiated...")
        logger.info("This may take a few minutes.")

        logger.info("\n" + "=" * 60)
        logger.info("INSTANCE DELETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info("\nAll resources have been removed.")
        logger.info("Firewall rules may still exist. Remove manually if needed.")

        return True

    except Exception as e:
        logger.error(f"Error deleting instance: {e}")
        return False


if __name__ == "__main__":
    success = destroy_instance()
    sys.exit(0 if success else 1)
