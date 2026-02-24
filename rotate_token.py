import os
import sys
import requests
from github import Github
from nacl import encoding, public

def encrypt_secret(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return encoding.Base64Encoder.encode(encrypted).decode("utf-8")

def perform_rotation():
    # 1. Get Environment Variables
    rancher_url = os.environ.get("RANCHER_URL")
    access_key = os.environ.get("RANCHER_ACCESS_KEY")
    secret_key = os.environ.get("RANCHER_SECRET_KEY")
    gh_token = os.environ.get("GH_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY") 

    if not all([rancher_url, access_key, secret_key, gh_token, repo_name]):
        print("Error: Missing required environment variables.")
        sys.exit(1)

    # 2. Login to Rancher / Generate Token
    auth = (access_key, secret_key)
    create_token_url = f"{rancher_url}/v3/tokens"
    
    token_payload = {
        "type": "token",
        "description": "Automated Rotation Token",
        "ttl": 0 
    }

    try:
        print(f"Requesting new token from {create_token_url}...")
        response = requests.post(create_token_url, json=token_payload, auth=auth)
        response.raise_for_status()
        data = response.json()
        
        # 'token' field usually contains the full bearer token value
        new_token_value = data.get("token")
        if not new_token_value:
            print("Error: content of 'token' field not found in response.")
            sys.exit(1)
            
        print("Successfully generated new Rancher token.")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to generate token: {e}")
        sys.exit(1)

    # 3. Update GitHub Secret
    try:
        print(f"Updating secret in GitHub repo: {repo_name}")
        g = Github(gh_token)
        repo = g.get_repo(repo_name)
        
        secret_name = "RANCHER_BEARER_TOKEN"
        
        # Get the repo's public key for secret encryption
        print("Fetching repository public key...")
        pub_key = repo.get_public_key()
        pub_key_id = pub_key.key_id
        pub_key_value = pub_key.key
        
        # Encrypt the token
        print("Encrypting new token...")
        encrypted_token = encrypt_secret(pub_key_value, new_token_value)
        
        # Update/Create the secret
        print(f"Uploading secret {secret_name}...")
        repo.create_secret(secret_name, encrypted_token)
        
        print(f"Successfully updated secret {secret_name}.")
        
    except Exception as e:
        print(f"Failed to update GitHub secret: {e}")
        sys.exit(1)

if __name__ == "__main__":
    perform_rotation()
