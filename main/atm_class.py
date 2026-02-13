# ATM definition
import re
from user_class import User
from  account_class import Account

class ATM:    
    def ATM(self):
        self.is_admin = False
        self.is_logged_in = False
        self.users = []
        self.current_user = None
    
    def login(self):
        check_admin = True
        while (check_admin):
            session = input("Is this an admin session (Y/n)?: ")
            
            if (session == "Y"):
                is_admin = True
                check_admin = False
            elif (session.casefold == "n"):
                check_admin = False
            else:
                print("Error Inavalid Input")
        
        if (is_admin):
            print("Logging in as admin")
            self.is_logged_in = True
            return
        
        check_user = True
        
        while (check_user):
            name = input("Please enter user name: ")
            
            for user in self.users:
                if (user.name == name):
                    check_user = False
                    self.current_user = user
                    break
            
            if (check_user):
                print("Error incorrect user name")
                
        self.is_logged_in = True
        print (f"Welcome {self.current_user.name}!")
    
    def logout(self):
        pass
    
    def main_menu(self):
        while(True):
            print("------ATM SYSTEM-----")
            print("1. Withdraw")
            print("2. Deposit")
            print("3. Transfer")
            print("4. Paybill")
            
            if (self.is_admin):
                print("5. Create Account")
                print("6. Delete Account")
                print("7. Disable Account")
                print("8. Change Account Plan")
            
            print("Q. Logout")
                
            choice = input("Please enter your chosen operation: ")
            
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
        with open("accounts") as file:
            next(file)
            
            for line in file:
                if (line == "00000_END_OF_FILE__________D_00000000"):
                    break
                
                number = line[:5]
                name = line[6:26]
                status = line[27:28]
                balance = line[29:]
                
                first_index = -1
                match = re.search(r'[^0]', number)
                if match:
                    first_index = match.start()
                
                number = number[first_index:]
                
                name = re.sub(r'([_])\1+', r'\1', name,)
                name = name.replace("_", " ")
                name = name.strip()
                
                first_index = -1
                match = re.search(r'[^0]', balance)
                if match:
                    first_index = match.start()
                    
                balance = balance[first_index:]
                
                account = Account(name, number, balance, "NP", status)
                
                in_list = False
                for user in self.users:
                    if user.name == name:
                        user.accounts.append(account)
                        in_list = True
                        break
                    
                if (not in_list):
                    self.users.append(User(name, "", [account]))