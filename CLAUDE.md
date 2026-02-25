# CLAUDE.md - Project Instructions

This file provides guidance for working on the SRE Rancher Token Renewal project.

## Project Overview

This project automates the renewal of Rancher API tokens using Terraform and GitHub Actions.

## Codebase Summary

| File | Purpose |
|------|---------|
| `main.tf` | Terraform main configuration - creates/renews Rancher token |
| `variables.tf` | Terraform variable definitions |
| `providers.tf` | Terraform provider configuration |
| `.github/workflows/rancher-token-renewal.yml` | GitHub Actions workflow for automated execution |

## How to Plan Tasks

1. **Understand the goal** - Read the relevant Terraform files first
2. **Identify affected files** - Determine what needs to change
3. **Consider dependencies** - Check how changes might impact other parts
4. **Test strategy** - Plan how to verify the changes work
5. **Rollback plan** - Know how to revert if needed

For non-trivial tasks, use `EnterPlanMode` to explore the codebase and design an implementation approach.

## How to Test

### Local Testing

1. Install Terraform:
   ```bash
   brew install terraform  # macOS
   # or apt-get install terraform  # Linux
   ```

2. Set environment variables:
   ```bash
   export RANCHER_URL="https://rancher.example.com"
   export RANCHER_TOKEN="your_admin_token"
   export RANCHER_TOKEN_NAME="my-token"
   ```

3. Initialize and apply Terraform:
   ```bash
   terraform init
   terraform plan
   terraform apply
   ```

### GitHub Actions Testing

1. Use `workflow_dispatch` to trigger manually:
   - Go to Actions tab in GitHub
   - Select "Rancher Token Renewal"
   - Click "Run workflow"

2. Check workflow logs for:
   - Terraform initialization success
   - Token creation/update confirmation
   - Any error messages

## How to Execute

### Local Execution

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply
```

### GitHub Actions Execution

The workflow runs automatically:
- **Schedule**: Daily at midnight UTC (configurable in workflow)
- **Manual**: Use `workflow_dispatch` trigger

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RANCHER_URL` | Yes | - | Rancher instance URL |
| `RANCHER_TOKEN` | Yes | - | Rancher API token with admin privileges |
| `RANCHER_TOKEN_NAME` | Yes | - | Name for the token resource |
| `token_description` | No | "Managed by Terraform" | Token description |
| `token_ttl` | No | 86400000 | Token TTL in milliseconds (24 hours) |

## Common Operations

### Modifying the GitHub Workflow

Edit `.github/workflows/rancher-token-renewal.yml`:
- Change schedule with cron syntax
- Add new variables to the `env` section
- Modify Terraform version if needed

### Updating Terraform Configuration

Edit `main.tf`, `variables.tf`, or `providers.tf`:
- Test locally first with `terraform plan`
- Verify changes work as expected
- Commit and push to trigger workflow

## Important Considerations

1. **Security**:
   - Never commit actual tokens
   - Use GitHub Secrets for all sensitive values
   - Store Terraform state remotely (S3, GCS) with encryption

2. **Token TTL**:
   - Default is 86400000 ms (24 hours)
   - Adjust based on your security requirements

3. **Error Handling**:
   - Check GitHub Actions logs for detailed error messages
   - Terraform will show errors in the workflow run

## Quick Reference

```bash
# Full local run
terraform init && terraform plan && terraform apply
```
