# CLAUDE.md - Project Instructions

This file provides guidance for working on the SRE Rancher Token Renew project.

## Project Overview

This project automates the rotation of Rancher API tokens and updates them in GitHub repository secrets. It consists of:

- **rotate_token.py** - Main Python script for token rotation
- **requirements.txt** - Python dependencies
- **.github/workflows/rotate-token.yml** - GitHub Actions workflow for automated execution

## Codebase Summary

### Core Components

| File | Purpose |
|------|---------|
| `rotate_token.py` | Main script - handles Rancher token creation and GitHub secret updates |
| `requirements.txt` | Dependencies: requests, PyGithub, PyNaCl |
| `.github/workflows/rotate-token.yml` | Weekly scheduled GitHub Actions workflow |

### Key Classes/Functions

- `RancherTokenRotator` class in `rotate_token.py`:
  - `validate_env()` - Validates required environment variables
  - `encrypt_secret()` - Encrypts token using GitHub public key
  - `get_rancher_token()` - Creates new Rancher API token
  - `update_github_secret()` - Updates GitHub repository secret
  - `run()` - Main execution flow

## How to Plan Tasks

1. **Understand the goal** - Read the relevant code files first
2. **Identify affected files** - Determine what needs to change
3. **Consider dependencies** - Check how changes might impact other parts
4. **Test strategy** - Plan how to verify the changes work
5. **Rollback plan** - Know how to revert if needed

For non-trivial tasks, use `EnterPlanMode` to explore the codebase and design an implementation approach.

## How to Test

### Local Testing

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set required environment variables**:
   ```bash
   export RANCHER_URL="https://rancher.example.com"
   export RANCHER_ACCESS_KEY="your_access_key"
   export RANCHER_SECRET_KEY="your_secret_key"
   export GH_TOKEN="your_github_pat"
   export GITHUB_REPOSITORY="owner/repo"
   ```

3. **Run the script**:
   ```bash
   python rotate_token.py
   ```

### Dry Run / Debug Mode

The script currently doesn't have a dry-run mode. For testing:
- Use a test Rancher instance
- Use a test GitHub repository
- Verify secrets are updated correctly before using in production

### GitHub Actions Testing

1. Use `workflow_dispatch` to trigger manually:
   - Go to Actions tab in GitHub
   - Select "Rotate Rancher Token"
   - Click "Run workflow"

2. Check workflow logs for:
   - Token generation success
   - Secret update confirmation
   - Any error messages

## How to Execute

### Local Execution

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Set environment variables
export RANCHER_URL="https://rancher.example.com"
export RANCHER_ACCESS_KEY="your_access_key"
export RANCHER_SECRET_KEY="your_secret_key"
export GH_TOKEN="your_github_pat"
export GITHUB_REPOSITORY="owner/repo"

# Run the script
python rotate_token.py
```

### GitHub Actions Execution

The workflow runs automatically:
- **Schedule**: Weekly on Monday at 00:00 UTC
- **Manual**: Use `workflow_dispatch` trigger

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RANCHER_URL` | Yes | - | Rancher instance URL |
| `RANCHER_ACCESS_KEY` | Yes | - | Rancher API access key |
| `RANCHER_SECRET_KEY` | Yes | - | Rancher API secret key |
| `GH_TOKEN` | Yes | - | GitHub PAT with repo permissions |
| `GITHUB_REPOSITORY` | Yes | - | Target repo (owner/repo) |
| `RANCHER_BEARER_TOKEN` | No | `RANCHER_BEARER_TOKEN` | Secret name to update |
| `RANCHER_TOKEN_TTL` | No | `0` | Token TTL in milliseconds |

## Common Operations

### Adding a New Feature

1. Edit `rotate_token.py` - Add method to `RancherTokenRotator` class
2. Update `run()` method to integrate the new feature
3. Test locally with test credentials
4. Update README.md if needed

### Modifying the GitHub Workflow

Edit `.github/workflows/rotate-token.yml`:
- Change schedule with cron syntax
- Add new secrets to the `env` section
- Modify Python version if needed

### Updating Dependencies

Edit `requirements.txt` and test:
```bash
pip install -r requirements.txt
python rotate_token.py
```

## Important Considerations

1. **Security**:
   - Never commit actual credentials
   - Use GitHub Secrets for all sensitive values
   - The GH_TOKEN needs `repo` scope for secret management

2. **Idempotency**:
   - Each run creates a new token but doesn't revoke old ones
   - Consider adding token cleanup logic for production use

3. **Error Handling**:
   - Script exits with code 1 on - Check logs any failure
   for detailed error messages

4. **Token TTL**:
   - Default is 0 (never expires)
   - Set `RANCHER_TOKEN_TTL` in milliseconds (e.g., 86400000 = 24 hours)

## Quick Reference

```bash
# Full local run
pip install -r requirements.txt && \
export RANCHER_URL="..." RANCHER_ACCESS_KEY="..." \
RANCHER_SECRET_KEY="..." GH_TOKEN="..." GITHUB_REPOSITORY="..." && \
python rotate_token.py
```
