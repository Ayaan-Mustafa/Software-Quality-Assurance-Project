# Place to instantiate atm stuff

from atm_class import ATM


# Create the ATM, loads user accounts, and start the user session loop
def main():

    atm = ATM()

    # Load accounts
    atm.load_accounts()

    # Allow repeated sessions
    while True:
        atm.login()
        atm.main_menu()


if __name__ == "__main__":
    main()
