# Rancher Token Update Automation

This project automates the renewal of Rancher API tokens using Terraform and GitHub Actions.

## Overview

Rancher API tokens have a configurable lifetime and need to be renewed before expiration. This automation ensures tokens are automatically refreshed using Terraform infrastructure-as-code practices.

## Prerequisites

- Terraform >= 1.0
- Rancher >= 2.6
- GitHub repository with secrets configured
- GitHub Actions enabled

## Configuration

### Required GitHub Secrets

Configure the following secrets in your GitHub repository:

| Secret | Description |
|--------|-------------|
| `RANCHER_URL` | Rancher server URL (e.g., https://rancher.example.com) |
| `RANCHER_TOKEN` | Initial Rancher API token with admin privileges |
| `RANCHER_TOKEN_NAME` | Name for the token resource |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `token_description` | Description for the token | "Managed by Terraform" |
| `token_ttl` | Token time-to-live in milliseconds | 86400000 (24 hours) |

## Usage

### Manual Run

1. Go to GitHub Actions
2. Select "Rancher Token Renewal" workflow
3. Click "Run workflow"

### Automated Schedule

The workflow runs automatically based on the schedule defined in `.github/workflows/rancher-token-renewal.yml`. Default: daily at midnight UTC.

## Files

```
.
├── README.md
├── main.tf
├── variables.tf
├── providers.tf
└── .github/
    └── workflows/
        └── rancher-token-renewal.yml
```

## Security Considerations

- Token is stored in GitHub Secrets (encrypted at rest)
- Terraform state should be stored remotely (e.g., S3, GCS) with encryption
- Consider using a service account with minimal required permissions
- Token rotation frequency should match your security requirements
