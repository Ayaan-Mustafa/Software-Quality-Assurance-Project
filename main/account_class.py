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
    def __init__(self, name, number, balance, plan, enabled):
        self.name = name
        self.number = number
        self.balance = balance
        self.plan = plan
        self.enabled = enabled
    
    # Overload __str__
    def __str__(self):
        return (f"name: {self.name}\n"
                f"number: {self.number}\n"
                f"balance: {self.balance}\n"
                f"plan: {self.plan}\n"
                f"enabled: {self.enabled}\n")