# ATM definition
import re
from user_class import User
from  account_class import Account

class ATM:  

    def __init__(self):
        self.ATM()

    def ATM(self):
        self.is_admin = False       # true if in admin mode
        self.is_logged_in = False   # true if logged in
        self.users = []             # list of all users in system
        self.current_user = None    # the current user, if admin should be none
        self.transactions = []      # list of all proccessed trasactions in current session

    # --- Core Logic ---

    def login(self):
        # check if the user is logging in as admin
        check_admin = True
        while (check_admin):
            # user input
            session = input("Is this an admin session (Y/n)?: ")
            
            # if user is admin set is_admin as true and break loop
            if (session == "Y"):
                is_admin = True
                check_admin = False
            # if the user is not admin break loop
            elif (session.casefold == "n"):
                check_admin = False
            # if user entered incorrect input ask again
            else:
                print("Error Inavalid Input")
        
        # if the user is admin skip asking for name
        if (is_admin):
            print("Logging in as admin")
            self.is_logged_in = True
            return
        
        # get the current non-admin user
        check_user = True
        while (check_user):
            # user input
            name = input("Please enter user name: ")
            
            # check user input against all users in system
            for user in self.users:
                # if names match, set that user as current user
                if (user.name == name):
                    check_user = False
                    self.current_user = user
                    break
            
            # if the user was not found ask again
            if (check_user):
                print("Error incorrect user name")
        
        # set logged in to true and print welcome message
        self.is_logged_in = True
        print(f"Welcome {self.current_user.name}!")
    
    # Logout function which writes log, resets session, returns to reloggin screen.
    def logout(self):
        if not self.is_logged_in:
            print("ERROR: not logged in.")
            return

        # TODO Write to transaction file
        # self.make_output_file()

        # Reset session state
        self.is_logged_in = False
        self.is_admin = False
        self.current_user = None

        print("Session ended. Logged out successfully.")
    
    def main_menu(self):
        # main menu loop
        while(True):
            # print meny
            print("------ATM SYSTEM-----")
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Transfer")
            print("4. Paybill")
            
            # display admin options only if admin
            if (self.is_admin):
                print("5. Create Account")
                print("6. Delete Account")
                print("7. Disable Account")
                print("8. Change Account Plan")
            
            print("Q. Logout")
            
            # user input
            choice = input("Please enter your chosen operation: ")
            
            # match input to choice
            if (choice == "1"):
                self.withdraw()
            elif (choice == "2"):
                self.deposit()
            elif (choice == "3"):
                self.transfer()
            elif (choice == "4"):
                self.paybill
            elif (choice == "5" and self.is_admin == True):
                self.create()
            elif (choice == "6" and self.is_admin == True):
                self.delete()
            elif (choice == "7" and self.is_admin == True):
                self.disable()
            elif (choice == "8" and self.is_admin == True):
                self.changeplan()
            elif (choice == "Q"):
                self.logout()
            else:
                print("Error invalid selection")
            
    
    # User withdraw money from own account
    def withdraw(self):

        # make sure the user is logged in
        if not self._require_login():
            return

        # get the account to withdraw from
        selected_account = self.get_current_user_account()

        # Make sure its not disabled
        if self._is_account_disabled(selected_account):
            print("ERROR: account is disabled.")
            return

        # print current balance
        print(f"Current account balance: ${selected_account.balance}")
        
        # init input variable
        amount = ""
        # loop condition
        check_amount = True
        while (check_amount):
            # user input
            amount = input("Enter amount to withdraw: ")
            amount = int(amount)
            
            # if the ammount is valid
            if (amount > 0 and amount <= 500 and amount <= selected_account.balance):
                # calculate new account balance
                new_balance = selected_account.balance - amount
                
                # loop over users to find account holder
                for i in range(len(self.users)):
                    if (self.user[i].name == selected_account.name):
                        # loop over holder's accounts
                        for j in range(len(self.users[i].accounts)):
                            # if the accounts matches
                            if (self.users[i].accounts[j].number == selected_account.number):
                                # print transaction
                                print(f"{selected_account.balance} - {amount} = {new_balance}")
                                # change the account balance
                                self.users[i].accounts[j].balance = new_balance
                                # print message
                                print("withdraw succesful")
                                # log transaction
                                self.write_log(code="01",
                                               name=selected_account.name, 
                                               number=selected_account.number, 
                                               funds=str(new_balance), 
                                               misc="NA")
                                # exit
                                return
            # otherwise print error message
            else:
                print("Error enter a valid amount")
            
    
    # Deposit money into an account owned by the user
    def deposit(self):
        
        # Make sure the user is logged in
        if not self._require_login():
            return

        # Get the account
        account = self.get_account()
        
        # Make sure its not disabled
        if self._is_account_disabled(account):
            print("ERROR: account is disabled.")
            return

        # make sure amount was positive
        amount = self._validate_positive_int("Enter amount to deposit: ")
        if amount is None:
            return

        # Update the balance
        old_balance = int(account.balance)
        new_balance = old_balance + amount
        account.balance = new_balance

        #Print balance
        print(f"{old_balance} + {amount} = {new_balance}")
        #Print deposit success
        print("Deposit successful")

        #Log
        self.write_log(code="04",
                    name=account.name,
                    number=account.number,
                    funds=str(amount),
                    misc="NA")
    

    #Transfer money from one account to another
    def transfer(self):
        
        # Ensure the user is logged in
        if not self._require_login():
            return

        #Select the from account
        print("Select FROM account:")
        from_account = self.get_account()

        # Make sure the account isnt disabled
        if self._is_account_disabled(from_account):
            print("ERROR: FROM account is disabled.")
            return

        # get the to account
        to_account_num = input("Enter TO account number: ").strip()
        to_account = self._find_account_by_number(to_account_num)

        #Make sure the account exists
        if to_account is None:
            print("ERROR: TO account not found.")
            return
        
        # Make sure the TO account is not disabled
        if self._is_account_disabled(to_account):
            print("ERROR: TO account is disabled.")
            return

        # Get the amount for transfer
        amount = self._validate_positive_int("Enter amount to transfer: ")
        if amount is None:
            return

        # Transfer cap
        if (not self.is_admin) and amount > 1000:
            print("ERROR: standard transfer max is $1000.")
            return

        # Make sure there is enough in the account
        if amount > int(from_account.balance):
            print("ERROR: insufficient funds.")
            return

        # Update the accounts money
        from_account.balance = int(from_account.balance) - amount
        to_account.balance = int(to_account.balance) + amount

        print(f"Transfer successful: {amount} from {from_account.number} to {to_account.number}")

        # Write log, funds = amount moved, misc = destination account
        self.write_log(code="02",
                    name=from_account.name,
                    number=from_account.number,
                    funds=str(amount),
                    misc=to_account.number)
    
    # Pay a bill from a selected account
    def paybill(self):

        # make sure the user is logged in
        if not self._require_login():
            return

        # get the account
        account = self.get_account()

        # make sure its not disabled
        if self._is_account_disabled(account):
            print("ERROR: account is disabled.")
            return

        # Enter the company code
        company = input("Enter company code (EC/CQ/FI): ").strip().upper()
        # Validate entry
        if company not in ("EC", "CQ", "FI"):
            print("ERROR: invalid company code.")
            return

        # Get the amount and ensure positive
        amount = self._validate_positive_int("Enter amount to pay: ")
        if amount is None:
            return

        # Make sure under max for bill
        if amount > 2000:
            print("ERROR: max paybill is $2000.")
            return

        # Make sure there is enough money in the account
        if amount > int(account.balance):
            print("ERROR: insufficient funds.")
            return

        # Update the account balance
        account.balance = int(account.balance) - amount
        #Output success
        print(f"Paybill successful: {amount} to {company} from {account.number}")

        #write log
        self.write_log(code="03",
                    name=account.name,
                    number=account.number,
                    funds=str(amount),
                    misc=company)
    
    
    # Admin only function to create an account for a user (both new or existing)
    def create(self):

        # Make sure the user is an admin
        if not self._require_admin():
            return

        # Get the account holder name, account num and plan
        name = input("Enter account holder name: ").strip()
        number = input("Enter new account number: ").strip()
        plan = input("Enter plan (NP/SP): ").strip().upper()

        # Validate plan
        if plan not in ("NP", "SP"):
            print("ERROR: invalid plan.")
            return

        # Ensure account number is unique
        if self._find_account_by_number(number) is not None:
            print("ERROR: account number already exists.")
            return

        # Enter the initial balance (must be positive)
        balance = self._validate_positive_int("Enter initial balance: ")
        if balance is None:
            return

        # make the new account
        new_account = Account(name, number, balance, plan, True)

        # attach to existing user or create new user
        for user in self.users:
            if user.name == name:
                user.accounts.append(new_account)
                print("Account created successfully.")
                self.write_log(code="05", name=name, number=number, funds=str(balance), misc=plan)
                return
            
        # otherwise make a new user
        self.users.append(User(name, "", [new_account]))
        print("Account created successfully.")
        #Log
        self.write_log(code="05", name=name, number=number, funds=str(balance), misc=plan)
    
    # Admin only function to delete a users account
    def delete(self):
        
        # Ensure the user is an admin
        if not self._require_admin():
            return

        # get the name and account number for the account
        name = input("Enter account holder name: ").strip()
        number = input("Enter account number to delete: ").strip()

        # find the user
        target_user = None
        for user in self.users:
            if user.name == name:
                target_user = user
                break

        # Handle no user found
        if target_user is None:
            print("ERROR: unknown account holder.")
            return

        # remove the account
        for i, account in enumerate(target_user.accounts):
            if account.number == number:
                del target_user.accounts[i]
                print("Account deleted successfully.")
                #Log
                self.write_log(code="06", name=name, number=number, funds="0", misc="NA")
                return

        print("ERROR: account not found for that user.")
    
    # Admin only function to disable an account
    def disable(self):
        
        # Ensure the user is an admin
        if not self._require_admin():
            return

        # get the account name and number
        name = input("Enter account holder name: ").strip()
        number = input("Enter account number to disable: ").strip()

        # find the user
        target_user = None
        for user in self.users:
            if user.name == name:
                target_user = user
                break

        # Handle user not found
        if target_user is None:
            print("ERROR: unknown account holder.")
            return

        # Disable the account
        for acct in target_user.accounts:
            if acct.number == number:
                acct.enabled = False
                print("Account disabled successfully.")
                #Log
                self.write_log(code="07", name=name, number=number, funds="0", misc="NA")
                return

        print("ERROR: account not found for that user.")

    # Admin only function to change the account plan
    def changeplan(self):

        # Ensure user is an admin
        if not self._require_admin():
            return

        # Get the name for account, account number and the new plan
        name = input("Enter account holder name: ").strip()
        number = input("Enter account number: ").strip()
        new_plan = input("Enter new plan (NP/SP): ").strip().upper()

        # Validate account plan given
        if new_plan not in ("NP", "SP"):
            print("ERROR: invalid plan.")
            return

        # find the user
        target_user = None
        for user in self.users:
            if user.name == name:
                target_user = user
                break

        # Handle user not found
        if target_user is None:
            print("ERROR: unknown account holder.")
            return

        # Change the plan for the account
        for acct in target_user.accounts:
            if acct.number == number:
                acct.plan = new_plan
                print("Plan changed successfully.")
                self.write_log(code="08", name=name, number=number, funds="0", misc=new_plan)
                return

        # handle account not found
        print("ERROR: account not found for that user.")
    
    # TODO? Maybe?
    def make_output_file(self):
        pass
    
    def load_accounts(self):
        # open accounts file
        with open("accounts") as file:
            # skip first line
            next(file)
            
            # read each line
            for line in file:
                # skip last line
                if (line == "00000_END_OF_FILE__________D_00000000"):
                    break
                
                # slice each line
                number = line[:5]
                name = line[6:26]
                status = line[27:28]
                enabled = (status == "A")
                balance = line[29:]
                
                # trim off leading 0 of number
                first_index = -1
                match = re.search(r'[^0]', number)
                if match:
                    first_index = match.start()
                
                number = number[first_index:]
                
                # remove and replace trailing underscores of name
                name = re.sub(r'([_])\1+', r'\1', name,)
                name = name.replace("_", " ")
                name = name.strip()
                
                # trim off leading zeros of balance
                first_index = -1
                match = re.search(r'[^0]', balance)
                if match:
                    first_index = match.start()
                    
                balance = balance[first_index:]
                
                # create account object
                account = Account(name, number, balance, "NP", enabled)
                
                # check if the user the account belongs to is in the users list
                in_list = False
                for user in self.users:
                    # if they are add the account to their list of acounts
                    if user.name == name:
                        user.accounts.append(account)
                        in_list = True
                        break
                
                # if user is not in the list add them with the account
                if (not in_list):
                    self.users.append(User(name, "", [account]))




    # --- Helpers ---

    # Check to see if the user is logged in. If yes return true, if not return false.
    def _require_login(self) -> bool:
        if not self.is_logged_in:
            print("ERROR: you must login first.")
            return False
        return True
    
    # Valiidation to ensure money is strictly > 0
    def _validate_positive_int(self, prompt: str):
        string = input(prompt).strip()
        try:
            amount = int(string)
        except ValueError:
            print("ERROR: invalid amount.")
            return None
        if amount <= 0:
            print("ERROR: amount must be > 0.")
            return None
        return amount

    # Checks if account is disabled. True = Yes, False = no
    def _is_account_disabled(self, account) -> bool:
        return not account.enabled

    # Helper function to ensure the user is an admin (useful before admin functions)
    def _require_admin(self) -> bool:
        if not self._require_login():
            return False
        if not self.is_admin:
            print("ERROR: admin only.")
            return False
        return True
    
    # Find any users account based on the number
    def global_find_account_by_number(self, acct_number: str):
        for user in self.users:
            for account in user.accounts:
                if account.number == acct_number:
                    return account
        return None
        
    def get_current_user_account(self):
        # selected account is the account to return
        selected_account = None
        # selected user is the user who the account belongs to
        # by default the current user
        selected_user = self.current_user
        # name of the account holder (only needed if admin)
        name = ""
        
        # if admin get the name of the user
        if (self.is_admin):
            # loop condition
            check_name = True
            
            # ask for name until valid name is inputed
            while (check_name):
                # user input
                name = input("Enter name of account holder")
                
                # check if user is in list
                for user in self.users:
                    # if the user is in the list
                    if (user.name == name):
                        # set the selected user
                        selected_user = user
                        # set the loop condition to false
                        check_name = False
                        # break the loop
                        break
                
                # error message
                if (check_name):
                    print("Error incorrect user name")
        
        # account number
        number = ""
        # loop condition
        check_number = True
        
        # ask for account number until valid number is inputed
        while (check_number):
            # user inpu
            number = input("Enter the account number")
            
            # loop over acconts held by user
            for account in selected_user.accounts:
                # if the user has the account that matches the number
                if (account.number == number):
                    # set selected account
                    selected_account = account
                    # set loop condition to false
                    check_number = False
                    # break the loop
                    break

            # error message
            if (check_number):
                print("Error incorrect account number")
        
        # return the selected account
        return selected_account
    
    # method that writes a string representing a transaction
    # and adds it to the transaction list
    def write_log(self, code, name, number, funds, misc):
        # write log string
        log = code + "_"
        log = log + "{:<20}".format(name) + "_"
        log = log + number + "_"
        log = log + funds + "_"
        log = log + misc
        
        # add log string to transaction list
        self.transactions.append(log)
        