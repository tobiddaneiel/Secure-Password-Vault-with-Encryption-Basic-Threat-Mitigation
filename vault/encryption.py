# vault/encryption.py
import os
import json
import base64
from typing import Dict, Any
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# ---------- small helpers ----------
def _b64e(b: bytes) -> str:
    return base64.b64encode(b).decode("utf-8")

def _b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("utf-8"))

# ---------- key derivation (PBKDF2) ----------
def derive_key(password: str, salt: bytes, iterations: int = 600_000) -> bytes:
    """
    Derive a 32-byte key (AES-256) from a passphrase using PBKDF2-HMAC-SHA256.
    Iterations ~600k is slow enough for personal use; tune per device.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,             # 32 bytes -> AES-256
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode("utf-8"))

# ---------- encrypt/decrypt a JSON-serializable object ----------
def encrypt_json(plaintext_obj: Dict[str, Any], password: str, iterations: int = 600_000) -> Dict[str, Any]:
    """
    Encrypt a Python dict (vault) with AES-256-GCM.
    Returns a dict you can dump to JSON (salt, nonce, ciphertext, kdf info).
    """
    data = json.dumps(plaintext_obj, separators=(",", ":")).encode("utf-8")
    salt = os.urandom(16)     # per-encryption random salt
    key = derive_key(password, salt, iterations)
    nonce = os.urandom(12)    # 96-bit nonce for AES-GCM
    aesgcm = AESGCM(key)
    ct = aesgcm.encrypt(nonce, data, associated_data=None)

    return {
        "version": 1,
        "kdf": "pbkdf2-sha256",
        "iterations": iterations,
        "salt": _b64e(salt),
        "nonce": _b64e(nonce),
        "ciphertext": _b64e(ct),  # includes auth tag
    }

def decrypt_json(encrypted_record: Dict[str, Any], password: str) -> Dict[str, Any]:
    """
    Decrypts a record produced by encrypt_json back into a Python dict.
    Raises ValueError on wrong password or tampering.
    """
    try:
        salt = _b64d(encrypted_record["salt"])
        nonce = _b64d(encrypted_record["nonce"])
        ct = _b64d(encrypted_record["ciphertext"])
        iterations = int(encrypted_record.get("iterations", 600_000))
        key = derive_key(password, salt, iterations)
        aesgcm = AESGCM(key)
        data = aesgcm.decrypt(nonce, ct, associated_data=None)
        return json.loads(data.decode("utf-8"))
    except Exception as e:
        # Wrong password, corrupted file, or tampering
        raise ValueError("Decryption failed (wrong password or corrupted data).") from e
