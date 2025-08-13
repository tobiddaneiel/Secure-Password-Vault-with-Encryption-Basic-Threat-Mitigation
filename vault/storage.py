import json
import os

STORAGE_FILE = "vault_data.json"

def load_credentials():
    """Load credentials from JSON file."""
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r") as file:
        return json.load(file)

def save_credentials(data):
    """Save credentials to JSON file."""
    with open(STORAGE_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_credential(service, username, password):
    """Add a new credential."""
    data = load_credentials()
    data[service] = {"username": username, "password": password}
    save_credentials(data)

def get_credential(service):
    """Retrieve a credential by service name."""
    data = load_credentials()
    return data.get(service, None)
