# vault/cli.py
from getpass import getpass
from typing import Dict
from . import storage

def show_menu():
    print("\nPassword Vault")
    print("1. Add Credential")
    print("2. Retrieve Credential")
    print("3. List Services")
    print("4. Save & Exit")

def add_credential(vault: Dict[str, dict]):
    service = input("Service name: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    vault[service] = {"username": username, "password": password}
    print("✅ Added.")

def retrieve_credential(vault: Dict[str, dict]):
    service = input("Service to retrieve: ").strip()
    cred = vault.get(service)
    if cred:
        print(f"🔑 {service} -> username: {cred['username']}, password: {cred['password']}")
    else:
        print("❌ Not found.")

def list_services(vault: Dict[str, dict]):
    if not vault:
        print("No entries yet.")
        return
    print("Services:")
    for s in sorted(vault.keys()):
        print(f" - {s}")

def main():
    # Unlock
    master = getpass("Set or enter master password: ")

    # Load (decrypt if Day 3+, or read plaintext if Day 2 file exists)
    try:
        vault = storage.load_vault(master)
    except ValueError:
        print("❌ Wrong password or corrupted file.")
        return

    while True:
        show_menu()
        choice = input("Choose: ").strip()
        if choice == "1":
            add_credential(vault)
        elif choice == "2":
            retrieve_credential(vault)
        elif choice == "3":
            list_services(vault)
        elif choice == "4":
            storage.save_vault(vault, master)
            print("🔒 Saved (encrypted). Bye!")
            break
        else:
            print("Invalid option.")
