import os
import sys
import logging
import requests
from github import Github
from nacl import encoding, public
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

class RancherTokenRotator:
    """Handles the rotation of Rancher API tokens and updates GitHub repository secrets."""

    def __init__(self):
        self.rancher_url = os.environ.get("RANCHER_URL")
        self.access_key = os.environ.get("RANCHER_ACCESS_KEY")
        self.secret_key = os.environ.get("RANCHER_SECRET_KEY")
        self.gh_token = os.environ.get("GH_TOKEN")
        self.repo_name = os.environ.get("GITHUB_REPOSITORY")
        self.secret_name = os.environ.get("RANCHER_BEARER_TOKEN", "RANCHER_BEARER_TOKEN")
        self.token_ttl = int(os.environ.get("RANCHER_TOKEN_TTL", "0"))

    def validate_env(self) -> bool:
        """Verify all required environment variables are present."""
        missing = []
        if not self.rancher_url: missing.append("RANCHER_URL")
        if not self.access_key: missing.append("RANCHER_ACCESS_KEY")
        if not self.secret_key: missing.append("RANCHER_SECRET_KEY")
        if not self.gh_token: missing.append("GH_TOKEN")
        if not self.repo_name: missing.append("GITHUB_REPOSITORY")

        if missing:
            logger.error(f"Missing required environment variables: {', '.join(missing)}")
            return False
        return True

    def encrypt_secret(self, public_key: str, secret_value: str) -> str:
        """Encrypt a Unicode string using the public key for GitHub Secrets."""
        try:
            pub_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
            sealed_box = public.SealedBox(pub_key)
            encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
            return encoding.Base64Encoder.encode(encrypted).decode("utf-8")
        except Exception as e:
            logger.error(f"Encryption failed: {e}")
            raise

    def get_rancher_token(self) -> Optional[str]:
        """Request a new API token from Rancher."""
        auth = (self.access_key, self.secret_key)
        url = f"{self.rancher_url.rstrip('/')}/v3/tokens"
        
        payload = {
            "type": "token",
            "description": f"Automated Rotation Token - {os.environ.get('GITHUB_RUN_ID', 'manual')}",
            "ttl": self.token_ttl
        }

        try:
            logger.info(f"Requesting new token from {url}...")
            response = requests.post(url, json=payload, auth=auth, timeout=30)
            response.raise_for_status()
            
            token = response.json().get("token")
            if not token:
                logger.error("Response data did not contain 'token' field.")
                return None
                
            logger.info("Successfully generated new Rancher token.")
            return token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Rancher API request failed: {e}")
            return None

    def update_github_secret(self, new_token: str) -> bool:
        """Update the repository secret with the new Rancher token."""
        try:
            logger.info(f"Updating secret '{self.secret_name}' in GitHub repo: {self.repo_name}")
            g = Github(self.gh_token)
            repo = g.get_repo(self.repo_name)
            
            logger.info("Fetching repository public key...")
            pub_key = repo.get_public_key()
            
            logger.info("Encrypting new token...")
            encrypted_token = self.encrypt_secret(pub_key.key, new_token)
            
            logger.info(f"Uploading secret {self.secret_name}...")
            repo.create_secret(self.secret_name, encrypted_token)
            
            logger.info(f"Successfully updated secret {self.secret_name}.")
            return True
            
        except Exception as e:
            logger.error(f"GitHub API operation failed: {e}")
            return False

    def run(self):
        """Execute the full rotation flow."""
        if not self.validate_env():
            sys.exit(1)

        new_token = self.get_rancher_token()
        if not new_token:
            sys.exit(1)

        if not self.update_github_secret(new_token):
            sys.exit(1)

        logger.info("Rotation process completed successfully.")

if __name__ == "__main__":
    rotator = RancherTokenRotator()
    rotator.run()
