# Rancher Token Renewal Automation

This project automates the renewal of Rancher API tokens using either a Python script or Terraform, with GitHub Actions for scheduling.

## Overview

Rancher API tokens have a configurable lifetime and need to be renewed before expiration. This project provides two approaches for token automation:

1. **Python Script** - Direct API token rotation with GitHub Secrets integration
2. **Terraform** - Infrastructure-as-Code approach for token management

## Prerequisites

- Python 3.11+ (for Python script approach)
- Terraform >= 1.0 (for Terraform approach)
- Rancher >= 2.6
- GitHub repository with secrets configured
- GitHub Actions enabled

## Quick Start

### Option 1: Python Script

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables:
   ```bash
   export RANCHER_URL="https://rancher.example.com"
   export RANCHER_ACCESS_KEY="your_access_key"
   export RANCHER_SECRET_KEY="your_secret_key"
   export GH_TOKEN="your_github_pat"
   export GITHUB_REPOSITORY="owner/repo"
   ```
4. Run the script:
   ```bash
   python rotate_token.py
   ```

### Option 2: Terraform

1. Configure GitHub secrets:
   - `RANCHER_URL` - Rancher server URL
   - `RANCHER_TOKEN` - Initial API token with admin privileges
   - `RANCHER_TOKEN_NAME` - Name for the token resource

2. Run the GitHub Actions workflow manually or wait for scheduled run

## Configuration

### Python Script Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `RANCHER_URL` | Yes | Rancher instance URL |
| `RANCHER_ACCESS_KEY` | Yes | Rancher API access key |
| `RANCHER_SECRET_KEY` | Yes | Rancher API secret key |
| `GH_TOKEN` | Yes | GitHub PAT with repo permissions |
| `GITHUB_REPOSITORY` | Yes | Target repository (owner/repo) |
| `RANCHER_BEARER_TOKEN` | No | Secret name (default: RANCHER_BEARER_TOKEN) |
| `RANCHER_TOKEN_TTL` | No | Token TTL in milliseconds (default: 0) |

### Terraform Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `token_description` | Description for the token | "Managed by Terraform" |
| `token_ttl` | Token TTL in milliseconds | 86400000 (24 hours) |

## Files

```
.
├── README.md
├── CLAUDE.md
├── rotate_token.py           # Python script for token rotation
├── requirements.txt          # Python dependencies
├── main.tf                   # Terraform main configuration
├── variables.tf              # Terraform variables
├── providers.tf              # Terraform providers
└── .github/
    └── workflows/
        ├── rotate-token.yml          # Python script workflow
        └── rancher-token-renewal.yml # Terraform workflow
```

## GitHub Actions

### Python Script Workflow

- **Schedule**: Weekly on Monday at 00:00 UTC
- **Manual Trigger**: Available via workflow_dispatch

### Terraform Workflow

- **Schedule**: Daily at midnight UTC (configurable)
- **Manual Trigger**: Available via workflow_dispatch

## Security Considerations

- Tokens are stored in GitHub Secrets (encrypted at rest)
- Use GitHub PAT with minimal required permissions (`repo` scope for secrets)
- For Terraform: store state remotely (S3, GCS) with encryption
- Consider using service accounts with minimal required permissions
- Token rotation frequency should match your security requirements
