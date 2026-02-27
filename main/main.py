# Place to instantiate atm stuff
import sys
from atm_class import ATM


# Create the ATM, loads user accounts, and start the user session loop
def main():
    if (len(sys.argv) > 1):
        accounts_file = sys.argv[1]
        transactions_file = sys.argv[2]
        atm = ATM(accounts_file=accounts_file, transactions_file=transactions_file)
        
    else:
        atm = ATM()

    # Load accounts
    atm.load_accounts()

    # Allow repeated sessions
    while True:
        atm.login()
        atm.main_menu()


if __name__ == "__main__":
    main()
