class CustomerInformation:

    def __init__(self, username, password, account, name, account_type):
        self.username = username
        self.password = password
        self.account = account
        self.name = name
        self.account_type = account_type

    def display(self):
        if self.account:
            print('\nUser and Account details are as follows\n')
            print('Username      : '+self.username)
            print('Name          : '+self.name)
            print('Account number: '+str(self.account.account_number))
            print('Balance       : Rs '+str(self.account.balance))
        else:
            print('\nUser details are as follows\n')
            print('Username      : ' + self.username)
            print('Name          : ' + self.name)

