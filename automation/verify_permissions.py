#!/usr/bin/env python3
"""
Verify GCP service account permissions
"""

import yaml
import logging
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def load_config():
    """Load configuration"""
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)


def verify_permissions():
    """Verify service account has required permissions"""
    config = load_config()

    logger.info("=" * 60)
    logger.info("GCP SERVICE ACCOUNT PERMISSION VERIFICATION")
    logger.info("=" * 60)

    # Load credentials
    try:
        scopes = [
            'https://www.googleapis.com/auth/compute',
            'https://www.googleapis.com/auth/cloud-platform'
        ]

        credentials = service_account.Credentials.from_service_account_file(
            config['gcp']['credentials_path'],
            scopes=scopes
        )

        logger.info(f"\n✓ Credentials loaded successfully")
        logger.info(f"  Service Account: {credentials.service_account_email}")
        logger.info(f"  Project: {config['gcp']['project_id']}")

    except Exception as e:
        logger.error(f"\n✗ Failed to load credentials: {e}")
        return False

    # Test Compute Engine API access
    try:
        compute = discovery.build('compute', 'v1', credentials=credentials)
        project_id = config['gcp']['project_id']
        zone = config['gcp']['zone']

        logger.info(f"\n Testing Compute Engine API access...")

        # Try to list instances (read permission)
        logger.info(f"  → Testing list instances permission...")
        result = compute.instances().list(project=project_id, zone=zone).execute()
        logger.info(f"  ✓ List instances: SUCCESS")

        if 'items' in result:
            logger.info(f"    Found {len(result['items'])} existing instance(s)")

        # Try to get project info
        logger.info(f"\n  → Testing project access...")
        project = compute.projects().get(project=project_id).execute()
        logger.info(f"  ✓ Project access: SUCCESS")
        logger.info(f"    Project Name: {project.get('name', 'N/A')}")

        logger.info("\n" + "=" * 60)
        logger.info("✓ PERMISSIONS VERIFIED SUCCESSFULLY!")
        logger.info("=" * 60)
        logger.info("\nYou can now run: python deploy.py")
        logger.info("=" * 60)

        return True

    except HttpError as e:
        logger.error("\n" + "=" * 60)
        logger.error("✗ PERMISSION ERROR")
        logger.error("=" * 60)

        if e.resp.status == 401:
            logger.error("\nError 401: Unauthorized")
            logger.error("\nPossible causes:")
            logger.error("1. Permissions were just added - wait 2-5 minutes for propagation")
            logger.error("2. Service account needs new credentials after permission change")
            logger.error("3. Service account lacks required roles")
            logger.error("\nRequired IAM Roles:")
            logger.error("  • Compute Admin (roles/compute.admin)")
            logger.error("  • Service Account User (roles/iam.serviceAccountUser)")
            logger.error("\nSolutions:")
            logger.error("1. Wait a few minutes and try again")
            logger.error("2. Regenerate service account key in GCP Console")
            logger.error("3. Verify permissions in IAM console:")
            logger.error(f"   https://console.cloud.google.com/iam-admin/iam?project={project_id}")

        elif e.resp.status == 403:
            logger.error("\nError 403: Forbidden")
            logger.error("\nThe service account exists but lacks required permissions.")
            logger.error("\nAdd these roles in GCP IAM Console:")
            logger.error("  • Compute Admin")
            logger.error("  • Service Account User")

        else:
            logger.error(f"\nHTTP Error {e.resp.status}: {e}")

        logger.error("\n" + "=" * 60)
        logger.error("See TROUBLESHOOTING.md for detailed solutions")
        logger.error("=" * 60)

        return False

    except Exception as e:
        logger.error(f"\n✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    verify_permissions()
