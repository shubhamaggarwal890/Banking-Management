class TransactionInformation:

    def __init__(self, account, credit_type, amount):
        self.account = account
        self.credit = credit_type
        self.amount = amount
        self.balance = self.balance + amount

