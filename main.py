from account_information import AccountInformation
from customer_information import CustomerInformation
import os
import pickle


def credential_check(username, password):
    customer = open('customer_db', 'rb')
    all_customers = pickle.load(customer)
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


def add_account():
    print("\nTo add the account, fill the following details of the user,")
    i = 0
    while True:
        if i > 2:
            print("Too many invalid inputs. Logging out, GoodBye!!!")
            exit()
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
            exit()
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
    account = AccountInformation(get_account_number())
    customer = CustomerInformation(username, password, account, name, account_type)
    read_customer = open('customer_db', 'rb')
    all_customers = pickle.load(read_customer)
    all_customers.append(customer)
    write_customer = open('customer_db', 'wb')
    pickle.dump(all_customers, write_customer)
    print("\nAccount details saved successfully!!! "+name+" account number is "+str(account.account_number)+"\n")


def delete_account():
    username = input("\nTo delete the account, enter the username of the user: ")
    customer_db = open('customer_db', 'rb')
    customers = pickle.load(customer_db)
    customer_db.close()
    index = 0
    for i in customers:
        if i.username == username:
            del customers[index]
            customer_db = open('customer_db', 'wb')
            pickle.dump(customers, customer_db)
            print("\n"+username+" successfully deleted!!!\n")
            return
        index = index+1
    print("\n"+username+" was not found. Nothing was deleted!!!\n")


def modify_account():
    username = input("\nTo modify the account, enter the username of the user: ")
    customer_db = open('customer_db', 'rb')
    customers = pickle.load(customer_db)
    customer_db.close()
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
            customer_db = open('customer_db', 'wb')
            pickle.dump(customers, customer_db)
            print("\nDetails of " + username + " successfully modified!!!\n")
            return
        index = index + 1
    print("\n" + username + " was not found. Nothing was modified!!!\n")


def search_account(username):
    customer_db = open('customer_db', 'rb')
    customers = pickle.load(customer_db)
    customer_db.close()
    for i in customers:
        if i.username == username:
            if i.account:
                print("\nUser & Account details are")
                print("Username: "+i.username)
                print("Name: "+i.name)
                print("Account Number: "+str(i.account.account_number))
                print("Balance: Rs "+str(i.account.balance)+"\n")
            else:
                print("\nUser details are")
                print("Username: " + i.username)
                print("Name: " + i.name+"\n")
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
                add_account()
            elif choice == '2':
                delete_account()
            elif choice == '3':
                modify_account()
            elif choice == '4':
                username = input("\nTo display account details, enter the username of the user: ")
                search_account(username)
            else:
                goodbye_msg()
                break
        except Exception as e:
            print(e)


def account_balance(username, amount):
    customer_db = open('customer_db', 'rb')
    customers = pickle.load(customer_db)
    customer_db.close()
    index = 0
    for i in customers:
        if i.username == username:
            customers[index].account.balance = i.account.balance + amount
            customer_db = open('customer_db', 'wb')
            pickle.dump(customers, customer_db)
            return customers[index].account.balance
        index = index + 1


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
                    balance = account_balance(user.username, amount)
                    print("\nAmount successfully deposited. Current Balance is "+str(balance)+"\n")
                except ValueError or Exception as e:
                    print("\nInvalid input!!!\n")

            elif choice == '2':
                try:
                    amount = float(input("Enter the amount to be withdrawn: "))
                    if amount < 0:
                        raise ValueError
                    balance = account_balance(user.username, -amount)
                    print("\nAmount successfully withdrawn. Current Balance is "+str(balance)+"\n")
                except ValueError or Exception as e:
                    print("\nInvalid input!!!\n")

            elif choice == '3':
                customer_db = open('customer_db', 'rb')
                customers = pickle.load(customer_db)
                customer_db.close()
                for i in customers:
                    if i.username == user.username:
                        print("\nAccount Number: " + str(i.account.account_number))
                        print("Balance: Rs " + str(i.account.balance) + "\n")
                        break
            elif choice == '4':
                search_account(user.username)
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
        print("\nSorry invalid credentials. Goodbye!")


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
    welcome_msg()
