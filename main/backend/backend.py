"""
The Backend of the banking application. Reads in the files in the
Master Accounts file and the transactions in the daily transactions
file, performs the operations on the accounts and then updates the
Master Accounts File
"""


import sys
import os
import re
from print_error import log_constraint_error
from read import read_old_bank_accounts
from write import write_new_current_accounts

# Output of read_old_bank_accounts = self.accounts
# {
#     'account_number': account_number str,
#     'name': name str,
#     'status': status str,
#     'balance': balance float,
#     'total_transactions': transactions int,
#     'plan': plan_type str
# }


# Backend class that performs the backend operations
class Backend():
    """
    Backend Class
    This class performs all the backend operations of them banking application.
    It reads the master accounts file and the daily transaction files and
    performs the transaction on the accounts in the master file.

    Parameters:
        transactions_path: the file path to the daily transactions file.
        accounts_path: the file path to the master accounts file.
    """
    # Constructor

    def __init__(self, accounts_path, transactions_path):
        """
        class constructor that takes the paths to the master accounts
        and transaction files as arguments and initializes the lists
        used during class operations.
        """
        # store file paths
        self.accounts_path = accounts_path
        self.transactions_path = transactions_path

        # lists for storing accounts and transactions
        self.accounts = []
        self.transactions = []

    # main method that runs all the backend operations
    def run(self):
        """
        calls all the methods that make up a single run of the program.
        """
        # read the old master accounts file
        self.accounts = read_old_bank_accounts(self.accounts_path)
        # read the transaction file
        self.read_transactions(self.transactions_path)
        # perform the transactions on the accounts
        self.perform_transactions()
        # write the new accounts file
        write_new_current_accounts(self.accounts_path)

    # method that reads the transactions file and turns the contents into a
    # list of dictionaries where each line is a represented as dictionary
    # in the list
    def read_transactions(self, path):
        """
        method that reads the contents of the transactions file and adds each
        line as a dictionary to a list.
        """
        # check if the transactions file exits
        if not os.path.isfile(path):
            # if it does not exit progam
            log_constraint_error("transaction file does not exsist",
                                 "/main/backend/backend.py - Backend class - "
                                 "read transaction method", True)

        # otherwise if the file exits
        # open the transactions file
        with open(path, "r") as file:
            # read each line in the file
            for line in file:
                # if the line is the end of file line stop
                if line == "00____________________________00000000_NA":
                    break

                # slice each line
                code = line[:2]
                name = line[3:23]
                number = line[24:29]
                funds = line[30:38]
                misc = line[39:]

                # trim off leading 0 of number
                number = self.remove_leading_zeros(number)

                # remove and replace trailing underscores of name
                name = re.sub(r'([_])\1+', r'\1', name,)
                name = name.replace("_", " ")
                name = name.strip()

                # trim off leading zeros of funds
                funds = self.remove_leading_zeros(number)

                # create transaction dictionary
                transaction = {"code": code,
                               "name": name,
                               "account_number": number,
                               "funds": funds,
                               "misc": misc}

                # add the transaction to the list
                self.transactions.append(transaction)

    # method that performs each transaction in the transactions list on the
    # accounts in the accounts list
    def perform_transactions(self):
        """
        method that performs the transactions
        operationson each account. iterates through both lists and
        applies the relevant transaction on each account based on the
        transaction code.
        """
        # lists for holding accounts that wrere created/deleted
        deleted = []

        # loop over accounts
        for account in self.accounts:
            # loop over transactions
            for transaction in self.transactions:
                # if the transaction does not involve account
                if account["account_number"] != transaction["account_number"]:
                    continue

                # check transaction code
                # 01 - withdraw
                if (transaction["code"] == "01"):
                    # remove funds from balance
                    account["balance"] -= transaction["funds"]
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 02 - transfer
                elif (transaction["code"] == "02"):
                    # find the account that the funds were transfered to
                    for transfer_account in self.accounts:
                        if (
                            transfer_account["account_number"]
                            == transaction["misc"]
                        ):
                            # add the funds to the recipient account
                            account["balance"] -= transaction["funds"]
                            # remove the funds from the account
                            transfer_account["balance"] += transaction["funds"]
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 03 - paybill
                elif (transaction["code"] == "03"):
                    # remove funds from balance
                    account["balance"] -= transaction["funds"]
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 04 - deposit
                elif (transaction["code"] == "04"):
                    # add funds to balance
                    account["balance"] += transaction["funds"]
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 05 - create
                elif (transaction["code"] == "05"):
                    # create account dictionary
                    new_account = {}

                    # add account fields
                    new_account["name"] = transaction["name"]
                    new_account["account_number"] \
                        = transaction["account_number"]
                    new_account["status"] = "A"
                    new_account["balance"] = transaction["funds"]
                    new_account["plan"] = transaction["misc"]
                    new_account["total"] = 0

                    # add account to list
                    self.accounts.append(new_account)

                # 06 - delete
                elif (transaction["code"] == "06"):
                    # add deleted accounts to delted list
                    deleted.append(transaction)
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 07 - disable
                elif (transaction["code"] == "07"):
                    # set account status to disabled
                    account["status"] = "D"
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 08 - changeplan
                elif (transaction["code"] == "08"):
                    # change account plan
                    account["plan"] == transaction["misc"]
                    # increment the total transactions
                    account["total_transactions"] += 1

                # 00 - end of session
                elif (transaction["code"] == "00"):
                    continue

                # unknown transaction code
                else:
                    log_constraint_error("The transaction code "
                                         f"{transaction["code"]} "
                                         "does not match any known "
                                         "transaction codes",
                                         "main/backend/backend.py - "
                                         "Backend Class - "
                                         "perform_transactions method ",
                                         False)

        # remove the deleted accounts from the list of accounts
        for deleted_account in deleted:
            for account in self.accounts:
                if (
                    deleted_account["account_number"]
                    == account["account_number"]
                ):
                    self.accounts.remove(account)

    # helper method that removes the leading zeros from numeric fields
    def remove_leading_zeros(self, number):
        """
        helper method that removes the leading zeros from Strings.
        """
        first_index = -1
        match = re.serach(r'[^0]', number)
        if match:
            first_index = match.start()

        return number[first_index:]


# main
def main():
    """
    The main function that runs the backend program. It reads the command line
    arguments to get the file paths and then creates and runs the backend
    class to perform the operations.
    """

    # default file paths
    master_account_file_path = ""
    transactions_file_path = ""

    # check for command line arguments
    if len(sys.argv) > 1:
        # set file paths as given paths
        master_account_file_path = sys.argv[0]
        transactions_file_path = sys.argv[1]

    # create Backend object
    backend = Backend(master_account_file_path, transactions_file_path)
    # run backend operations
    backend.run()


if __name__ == "__main__":
    main()
