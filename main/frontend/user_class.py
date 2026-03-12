# User class stuff
class User:
    """
    Represents a user within the ATM system.

    A user possesses identification credentials and can hold multiple
    bank accounts associated with their profile.

    Attributes:
        name (str): The name of the user.
        pin (str): The personal identification number for the user.
        accounts (list): A list of Account objects belonging to this user.
    """
    name = ''
    pin = ''
    acounts = []

    # Creates a User including an account
    def __init__(self, name, pin, accounts):
        """
        Initializes a new User instance.

        Args:
            name (str): The name of the user.
            pin (str): The PIN for the user.
            accounts (list): A list of initial Account objects for the user.
        """
        self.name = name
        self.pin = pin
        self.accounts = accounts

    # Creates a User that doesn't have an account yet
    # def __init__(self, name, pin):
    #     self.name = name
    #     self.pin = pin
    #     self.accounts = []

    # Lists all the accounts for the user using its own tostring function
    def list_accounts(self):
        """
        Iterates through the user's accounts and prints the string
        representation of each one.
        """
        for i in self.accounts:
            print(i.__str__())

    # Can add an account to a User
    def add_account(self, new_account):
        """
        Appends a new account to the user's list of accounts.

        Args:
            new_account (Account): The Account object to be added to the user.
        """
        self.accounts.append(new_account)

    def __str__(self):
        """
        Generates a formatted string representation of the User.

        Returns:
            str: A multi-line string displaying the user's name, pin,
            and their associated accounts.
        """
        return (f"name: {self.name}\n"
                f"pin : {self.pin}\n"
                f"accounts:\n {self.accounts}")
