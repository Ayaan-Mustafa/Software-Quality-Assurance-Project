# User class stuff
class User:
    name = '' 
    pin = ''
    acounts = []

    #Creates a User including an account
    def User(self,name,pin,accounts):
        self.name = name
        self.pin = pin
        self.accounts = accounts

    #Creates a User that doesn't have an account yet
    def User(self,name,pin):
        self.name = name
        self.pin = pin
        self.accounts = []

    #Lists all the accounts for the user using its own tostring function
    def list_accounts(self):
        for i in self.accounts:
            print(i.__str__())

    #Can add an account to a User
    def add_account(self, new_account):
        self.accounts.append(new_account)
    
