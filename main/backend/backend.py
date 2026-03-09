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
    # Constructor
    def __init__(self, accounts_path, transactions_path):
        # store file paths
        self.accounts_path = accounts_path
        self.transactions_path = transactions_path

        # lists for storing accounts and transactions
        self.accounts = []
        self.transactions = []

    # main method that runs all the backend operations
    def run(self):
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
                misc = line[39:42]

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
        # lists for holding accounts that wrere created/deleted
        created = []
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
                    account["total_transactions"] += 1

                # 02 - transfer
                elif (transaction["code"] == "02"):
                    # TODO
                    account["total_transactions"] += 1

                # 03 - paybill
                elif (transaction["code"] == "03"):
                    # remove funds from balance
                    account["balance"] -= transaction["funds"]
                    account["total_transactions"] += 1

                # 04 - deposit
                elif (transaction["code"] == "04"):
                    # add funds to balance
                    account["balance"] += transaction["funds"]
                    account["total_transactions"] += 1

                # 05 - create
                elif (transaction["code"] == "05"):
                    # TODO
                    created.append(transaction)
                    account["total_transactions"] += 1

                # 06 - delete
                elif (transaction["code"] == "06"):
                    # TODO
                    deleted.append(transaction)
                    account["total_transactions"] += 1

                # 07 - disable
                elif (transaction["code"] == "07"):
                    # set account status to disabled
                    account["status"] = "D"
                    account["total_transactions"] += 1

                # 08 - changeplan
                elif (transaction["code"] == "08"):
                    # change account plan
                    account["plan"] == transaction["misc"]
                    account["total_transactions"] += 1

                # 00 - end of session
                elif (transaction["code"] == "00"):
                    continue

    # helper method that removes the leading zeros from numeric fields
    def remove_leading_zeros(self, number):
        first_index = -1
        match = re.serach(r'[^0]', number)
        if match:
            first_index = match.start()

        return number[first_index:]


# main
def main():
    # TODO
    pass


if __name__ == "__main__":
    main()
