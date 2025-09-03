import pytest
from vault import encryption

def test_encrypt_decrypt_roundtrip():
    data = {"username": "test_user", "password": "test_pass"}
    master_password = "strong_master_password"

    # Encrypt the data
    encrypted_data = encryption.encrypt_json(data, master_password)

    #assert encrypted_data != data  # Ensure data is actually encrypted
    #assert isinstance(encrypted_data, str)  # Ensure encrypted data is a string

    # Decrypt the data
    decrypted_data = encryption.decrypt_json(encrypted_data, master_password)

    assert decrypted_data == data  # Ensure round-trip integrity

def test_decrypt_with_wrong_password():
    data = {"username": "test_user", "password": "test_pass"}
    correct_password = "correct_password"
    wrong_password = "wrong_password"

    # Encrypt the data
    encrypted_data = encryption.encrypt_json(data, correct_password)

    # Attempt to decrypt with the wrong password
    with pytest.raises(ValueError):
        encryption.decrypt_json(encrypted_data, wrong_password)