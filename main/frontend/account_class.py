# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Name: Ayaan Mustafa
# Date: 2026/02/03
# Purpose: Define the Account class
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Account class
class Account:
    """
    Represents a single bank account within the ATM system.

    Stores the financial state and settings for a specific account,
    such as its balance, plan type, and active status.

    Attributes:
        name (str):
            The name of the account holder.
        number (str):
            The unique account number.
        balance (int or float):
            The current financial balance of the account.
        plan (str):
            The plan type associated with the account (e.g., "NP" or "SP").
        enabled (bool):
            True if the account is active/enabled, False if disabled.
    """
    # Class fields and default values
    name = "No_Name"
    number = "*****"
    balance = 0.0
    plan = "NP"
    enabled = True

    # Parameterized constructor
    def __init__(self, name, number, balance, plan, enabled):
        """
        Initializes a new Account instance with the provided details.

        Args:
            name (str): The name of the account holder.
            number (str): The account number.
            balance (int or float): The initial balance of the account.
            plan (str): The account plan type (e.g., 'NP', 'SP').
            enabled (bool): The operational status of the account.
        """
        self.name = name
        self.number = number
        self.balance = balance
        self.plan = plan
        self.enabled = enabled

    # Overload __str__
    def __str__(self):
        """
        Generates a formatted string representation of the Account.

        Returns:
            str: A multi-line string displaying the account's name, number,
            balance, plan type, and enabled status.
        """
        return (f"name: {self.name}\n"
                f"number: {self.number}\n"
                f"balance: {self.balance}\n"
                f"plan: {self.plan}\n"
                f"enabled: {self.enabled}\n")
