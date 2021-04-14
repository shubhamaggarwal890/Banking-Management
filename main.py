from account_information import AccountInformation
from customer_information import CustomerInformation
from transaction_information import TransactionInformation
import os
import pickle


def credential_check(username, password):
    customer = open('customer_db', 'rb')
    all_customers = pickle.load(customer)
    customer.close()
    for i in all_customers:
        if i.username == username and i.password == password:
            return i
    return None


def unique_username(username):
    customer = open('customer_db', 'rb')
    all_users = pickle.load(customer)
    for i in all_users:
        if i.username == username:
            return False
    return True


def get_account_number():
    account = open('account_db', 'r')
    account_number = int(account.read())
    account.close()
    account = open('account_db', 'w')
    account.write(str(account_number+1))
    account.close()
    return account_number


def get_customer_db():
    try:
        read_customer = open('customer_db', 'rb')
        all_customers = pickle.load(read_customer)
        read_customer.close()
        return all_customers
    except pickle.PickleError or Exception as e:
        return None


def write_customer_db(modified_customers):
    try:
        write_customer = open('customer_db', 'wb')
        pickle.dump(modified_customers, write_customer)
        write_customer.close()
        return True
    except pickle.PickleError or Exception as e:
        return False


def add_customer_info(username, password, name, account_type):
    try:
        account = AccountInformation(get_account_number())
        customer = CustomerInformation(username, password, account, name, account_type)
        all_customers = get_customer_db()
        all_customers.append(customer)
        if write_customer_db(all_customers):
            return account
    except AttributeError or Exception as e:
        return None


def delete_customer_info(username):
    try:
        customers = get_customer_db()
        index = 0
        for i in customers:
            if i.username == username:
                del customers[index]
                return write_customer_db(customers)
            index = index + 1
    except TypeError or Exception:
        return False
    return False


def add_customer_menu():
    print("\nTo add the account, fill the following details of the user,")
    i = 0
    while True:
        if i > 2:
            print("Too many invalid inputs. Logging out, GoodBye!!!")
            return
        username = input("Username: ")
        if unique_username(username):
            break
        print("User already present, please choose another username!!")
        i = i+1
    password = input("Password: ")
    name = input("Name: ")
    i = 0
    while True:
        if i > 2:
            print("Too many invalid inputs. Logging out, GoodBye!!!")
            return
        account_type = input("Press 1 for admin or 2 for user account type: ")
        if account_type == '1':
            account_type = True
            break
        elif account_type == '2':
            account_type = False
            break
        else:
            print("Invalid input!!!")
        i = i+1
    account = add_customer_info(username, password, name, account_type)
    if account:
        print("\nAccount details saved successfully!!! " + name + " account number is " + str(
            account.account_number) + "\n")
    else:
        print("\nSome error occurred!!! Please try again\n")


def delete_customer_menu():
    username = input("\nTo delete the account, enter the username of the user: ")
    if delete_customer_info(username):
        print("\n" + username + " successfully deleted!!!\n")
    else:
        print("\n" + username + " was not found. Nothing was deleted!!!\n")


def modify_account():
    username = input("\nTo modify the account, enter the username of the user: ")
    customers = get_customer_db()
    index = 0
    for i in customers:
        if i.username == username:
            print("Press 1 to change the password\nPress 2 to change the name\nPress any other key to exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                i.password = input("Enter the new password: ")
            elif choice == '2':
                i.name = input('Enter the name of the user: ')
            else:
                print("\nNothing was modified!!!\n")
                return
            customers[index] = i
            if write_customer_db(customers):
                print("\nDetails of " + username + " successfully modified!!!\n")
                return
            else:
                print("\nDetails couldn't be modified, some error occurred!!Please try again!!!\n")
            return
        index = index + 1
    print("\n" + username + " was not found. Nothing was modified!!!\n")


def search_account(username):
    customers = get_customer_db()
    for i in customers:
        if i.username == username:
            i.display()
            return
    print("\n" + str(username) + " was not found. Nothing to search!!!\n")


def admin_operations(user):
    print("\n-------------------Welcome ADMIN, " + user.name + "-------------------\n")
    while True:
        try:
            choice = input(
                "Press 1 to Add an account\nPress 2 to delete an account\nPress 3 to modify an account\n"
                "Press 4 to display account details\n"
                "Press any other key to exit\nEnter your choice: "
            )
            if choice == '1':
                add_customer_menu()
            elif choice == '2':
                delete_customer_menu()
            elif choice == '3':
                modify_account()
            elif choice == '4':
                username = input("\nTo display account details, enter the username of the user: ")
                search_account(username)
                print("\n")
            else:
                goodbye_msg()
                break
        except Exception as e:
            print(e)


def account_balance(username, amount):
    customers = get_customer_db()
    index = 0
    for i in customers:
        if i.username == username:
            customers[index].account.balance = i.account.balance + amount
            write_customer_db(customers)
            return customers[index].account
        index = index + 1


def make_transaction(account, credit_type, amount):
    if not os.path.isfile('transaction_db'):
        transaction = TransactionInformation(account, credit_type, amount)
        transaction_db = open('transaction_db', 'wb')
        pickle.dump([transaction], transaction_db)
    else:
        transaction_db = open('transaction_db', 'rb')
        transactions = pickle.load(transaction_db)
        transaction = TransactionInformation(account, credit_type, amount)
        transactions.append(transaction)
        transaction_db.close()
        transaction_db = open('transaction_db', 'wb')
        pickle.dump(transactions, transaction_db)
        transaction_db.close()


def get_account_transaction(account):
    transaction_db = open('transaction_db', 'rb')
    transactions = pickle.load(transaction_db)
    transaction_db.close()
    flag = False
    for t in transactions:
        if t.account.account_number == account.account_number:
            flag = True
            t.display()
    if not flag:
        print("\n-------------------No Transactions found-------------------")


def user_operations(user):
    print("\n-------------------Welcome " + user.name + "-------------------\n")
    print("Account number "+str(user.account.account_number)+"\n")
    while True:
        try:
            choice = input(
                "Press 1 to make a deposit\nPress 2 to make a withdraw\nPress 3 to view balance\n"
                "Press 4 to display account details\n"
                "Press any other key to exit\nEnter your choice: "
            )
            if choice == '1':
                try:
                    amount = float(input("Enter the amount to be deposited: "))
                    if amount < 0:
                        raise ValueError
                    account = account_balance(user.username, amount)
                    make_transaction(account, True, amount)
                    print("\nAmount successfully deposited. Current Balance is "+str(account.balance)+"\n")
                except ValueError or Exception as e:
                    print("\nInvalid input!!!\n")

            elif choice == '2':
                try:
                    amount = float(input("Enter the amount to be withdrawn: "))
                    if amount < 0:
                        raise ValueError
                    account = account_balance(user.username, -amount)
                    make_transaction(account, False, amount)
                    print("\nAmount successfully withdrawn. Current Balance is "+str(account.balance)+"\n")
                except ValueError or Exception as e:
                    print("\nInvalid input!!!\n")

            elif choice == '3':
                customers = get_customer_db()
                for i in customers:
                    if i.username == user.username:
                        print("\nAccount Number: " + str(i.account.account_number))
                        print("Balance: Rs " + str(i.account.balance))
                        print("\n-------------------Transactions-------------------\n")
                        get_account_transaction(i.account)
                        print("\n")
                        break
            elif choice == '4':
                search_account(user.username)
                print("\n")
            else:
                goodbye_msg()
                break
        except Exception as e:
            print(e)


def goodbye_msg():
    print("\nThankYou, Logging out. GoodBye!!!\n")


def welcome_msg():
    print("\n-------------------Welcome to Online Banking Management System-------------------\n")
    print("Please enter your credentials")
    username = input("Username: ")
    password = input("Password: ")
    logged_user = credential_check(username, password)
    if logged_user:
        if logged_user.account_type:
            admin_operations(logged_user)
        else:
            user_operations(logged_user)
    else:
        print("\nSorry invalid credentials. Goodbye!\n")


def initial_setup():
    if not os.path.isfile('customer_db'):
        admin = CustomerInformation('admin', 'admin', None, 'admin', True)
        file_customer = open('customer_db', 'wb')
        pickle.dump([admin], file_customer)
    if not os.path.isfile('account_db'):
        account = open('account_db', 'w')
        account.write(str(100000000001))
        account.close()


if __name__ == '__main__':
    initial_setup()
    while True:
        try:
            welcome_msg()
        except KeyboardInterrupt or Exception as e:
            print()
            exit()
