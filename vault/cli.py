from . import storage

def show_menu():
    print("\nPassword Vault")
    print("1. Add Credential")
    print("2. Retrieve Credential")
    print("3. Exit")

def add_credential():
    service = input("Enter service name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    storage.add_credential(service, username, password)
    print("Credential added successfully.")

def retrieve_credential():
    service = input("Enter service name to retrieve: ")
    cred = storage.get_credential(service)
    if cred:
        print(f"Username: {cred['username']}")
        print(f"Password: {cred['password']}")
    else:
        print("No credentials found for that service.")
