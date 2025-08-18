# main.py
from vault.cli import main
from getpass import getpass
from vault import storage

def main():
    master_passsword = getpass("Enter the master password to unlock the vault:  ")
    
    try:
        #Load and decrypt vault from disk to memory
        vault = storage.load_vault(master_password)
    except ValueError:
        print("X Wrong password or corrupted vault")
        return

    #Pass the in-memory vault and master password to the CLI
    main_cli(vault, master_password)

if __name__ == "__main__":
    main()
