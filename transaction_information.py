from datetime import datetime


class TransactionInformation:

    def __init__(self, account, credit_type, amount):
        self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.account = account
        self.credit = credit_type
        self.amount = amount

    def display(self):
        if self.credit:
            print(self.date + ' CREDIT Rs ' + str(self.amount))
        else:
            print(self.date + ' DEBIT  Rs ' + str(self.amount))
