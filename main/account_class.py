# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Name: Ayaan Mustafa
# Date: 2026/02/03
# Purpose: Define the Account class
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Account class
class Account:
    # Class fields and default values
    name = "No_Name"
    number = "*****"
    balance = 0
    plan = "NP"
    enabled = True
    
    # Parameterized constructor
    def Account (self, name, number, balance, plan, enabled):
        self.name = name
        self.number = number
        self.balance = balance
        self.plan = plan
        self.enabled = enabled
    
    # Overload __str__
    def __str__(self):
        return f"""name: {self.name}
    number: {self.number}
    balance: {self.balance}
    plan: {self.plan}
    enabled: {self.enabled}"""