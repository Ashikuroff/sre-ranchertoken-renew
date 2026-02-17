# SRE Rancher Token Renew

This project automates the rotation of Rancher API tokens and updates them in GitHub repository secrets. This ensures that CI/CD pipelines and other automated processes maintain secure and continuous access to Rancher resources without manual intervention.

## Features
- **Automated Rotation**: Generates a new Rancher API token using existing credentials.
- **GitHub Integration**: Automatically updates the `RANCHER_BEARER_TOKEN` secret in the specified GitHub repository.
- **Configurable**: Environment variables allow for easy configuration of URL, keys, and token properties.
- **Logging**: Detailed logging for monitoring and troubleshooting.

## Setup

### Environment Variables

The following environment variables are required for the script to run:

| Variable | Description |
| :--- | :--- |
| `RANCHER_URL` | The base URL of your Rancher instance (e.g., `https://rancher.example.com`). |
| `RANCHER_ACCESS_KEY` | Your Rancher API Access Key. |
| `RANCHER_SECRET_KEY` | Your Rancher API Secret Key. |
| `GH_TOKEN` | A GitHub Personal Access Token (PAT) with `repo` permissions to update secrets. |
| `GITHUB_REPOSITORY` | The full name of the GitHub repository (e.g., `owner/repo`). |
| `RANCHER_BEARER_TOKEN` | (Optional) The name of the secret to update. Defaults to `RANCHER_BEARER_TOKEN`. |
| `RANCHER_TOKEN_TTL` | (Optional) The TTL for the new token in milliseconds. Defaults to `0` (never expires). |

### GitHub Actions

The provided workflow `.github/workflows/rotate-token.yml` is configured to run weekly. Ensure the required secrets are set in your GitHub repository's "Actions secrets and variables" settings.

## Local Execution

To run the script locally:

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Export the required environment variables.
3. Run the script:
   ```bash
   python rotate_token.py
   ```
