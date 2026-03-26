"""
The frontend of the banking application. Reads the accounts from the bank
accounts file and allows the user to perform various transactions on them
and logs the results. Once the user is done the program exits and writes all
the transaction logs to a transaction file.

Inputs:
Bank Accounts file, a txt file that stores all the bank accounts in a specific
format

Command line input from the user, the users instructions to the program in
text form

Outputs:
Text in the command line to instruct the user on how to use the program and to
show them the results of their operations

Transaction file detailing all the transactions that took place in that session

Run Instructions
run using the basic python command from the frontend directory
"""

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
