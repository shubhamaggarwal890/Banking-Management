from datetime import datetime


class TransactionInformation:

    def __init__(self, account, credit_type, amount):
        self.date = datetime.strftime("%d/%m/%Y %H:%M:%S")
        self.account = account
        self.credit = credit_type
        self.amount = amount

    def display(self):
        print(self.date+' '+str(self.account.account_number)+' C Rs' if self.credit else ' D Rs'+str(self.amount))

