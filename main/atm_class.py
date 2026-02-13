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

    # --- Helpers ---
    # Check to see if the user is logged in. If yes return true, if not return false.
    def _require_login(self) -> bool:
        if not self.is_logged_in:
            print("ERROR: you must login first.")
            return False
        return True
    

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
            
    
    def withdraw(self):
        pass
    
    def deposit(self):
        pass
    
    def transfer(self):
        pass
    
    def paybill(self):
        pass
    
    def create(self):
        pass
    
    def delete(self):
        pass
    
    def disable(self):
        pass
    
    def changeplan(self):
        pass
    
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
                account = Account(name, number, balance, "NP", status)
                
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
        
        