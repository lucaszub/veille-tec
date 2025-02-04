from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# URL de ton Key Vault
key_vault_url = "https://keyveille.vault.azure.net/"

# Créer un client pour accéder au Key Vault
credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

def get_youtube_api_key(secret_name="youtube-key"):
    """Récupère la clé API YouTube depuis Azure Key Vault."""
    # Récupérer le secret
    retrieved_secret = secret_client.get_secret(secret_name)
    return retrieved_secret.value
