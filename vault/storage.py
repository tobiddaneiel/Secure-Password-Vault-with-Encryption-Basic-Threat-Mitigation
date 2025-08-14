# vault/storage.py
import json
import os
from typing import Dict, Any
from . import encryption

STORAGE_FILE = "vault_data.json"   # stays in project root

def _is_encrypted_blob(obj: Any) -> bool:
    # Detects Day 3+ encrypted format
    return isinstance(obj, dict) and {"ciphertext", "salt", "nonce"} <= set(obj.keys())

def load_vault(password: str) -> Dict[str, Any]:
    """
    Load and decrypt the entire vault dict from disk.
    If file doesn't exist -> return empty dict.
    If file is legacy plaintext JSON -> return it (Day 2) and re-encrypt on next save.
    """
    if not os.path.exists(STORAGE_FILE):
        return {}

    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        obj = json.load(f)

    if _is_encrypted_blob(obj):
        # Day 3+ encrypted file
        return encryption.decrypt_json(obj, password)
    else:
        # Day 2 plaintext (migration path)
        return obj if isinstance(obj, dict) else {}

def save_vault(vault_dict: Dict[str, Any], password: str) -> None:
    """
    Encrypt and save the entire vault dict to disk using the master password.
    """
    enc = encryption.encrypt_json(vault_dict, password)
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(enc, f, indent=2)
