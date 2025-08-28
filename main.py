# main.py
import logging
from vault.cli import main_cli
from getpass import getpass
from vault import storage

def main():
    #Configure logging
    logging.basicConfig(filename="failed_attempts.log", level=logging.WARNING, format="%(asctime)s - %(message)s")

    MAX_ATTEMPTS = 3
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        master_password = getpass("Enter the master password to unlock the vault:  ")
        try:
            #Load and decrypt vault from disk to memory
            vault = storage.load_vault(master_password)
            break #successful login
        except ValueError:
            print("X Wrong password or corrupted vault")
            attempts += 1
            logging.warning(f"Failed login attempt #{attempts}")
            print(f"Wrong password ({attempts}/{MAX_ATTEMPTS})")
        
    if attempts >= MAX_ATTEMPTS:
        print("Account locked due to multiple failed login attempts.")
        exit(1)

    #Pass the in-memory vault and master password to the CLI
    main_cli(vault, master_password)

if __name__ == "__main__":
    main()
