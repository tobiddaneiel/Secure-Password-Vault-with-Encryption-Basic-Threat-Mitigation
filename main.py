from vault import cli

def main():
    while True:
        cli.show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            cli.add_credential()
        elif choice == "2":
            cli.retrieve_credential()
        elif choice == "3":
            print("Exiting Password Vault.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
