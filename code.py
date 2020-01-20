from getpass import getpass
import csv


def init():
    print("Press 1: Create Account")
    print("Press 2: Transaction")
    print("Press 0: Exit")
    user_input = input("")
    if user_input == "1":
        create_account()
    if user_input == "2":
        login()
    if user_input == "0":
    	exit()

def register_email():
    email = input("Enter Email: ")
    with open("bank.csv", "r") as f:
        data_reader = csv.reader(f)
        for row in data_reader:
            if row:
                if email == row[0]:
                    print("Email already exists")
                    register_email()
                    # email = input("Enter another Email: ")
    return email
        
        
def register_password():    
    password = getpass("Enter Password: ")
    confirmpassword = getpass("Confirm Password: ")
    if password != confirmpassword:
        print("Passwords do not match!")
        register_password()
    else:
        return password

def create_account():
    email =  register_email()
    password = register_password()
    with open("bank.csv", "a") as f:
        data_writer = csv.writer(f)
        data_writer.writerow([email, password, 0.0])
    print("Account Created \n")
    init()

def login():
    auth_email = input("enter your email: ")
    auth_pass =  getpass("enter your password: ")
    with open("bank.csv", "r") as f:
        data_reader = list(csv.reader(f))
        data_reader = [i for i in data_reader if i]
        emails = [i[0] for i in data_reader[1:] if i ]
        try:
            email_index = emails.index(auth_email) + 1
            if auth_pass != data_reader[email_index][1]:
                print("Invalid Email or Password")
                init()
            else:
                print("Login Succesful")
                transaction(email_index, data_reader)
        except ValueError:
            print("Account does not exist")
            init()

def check_balance(data_reader, email_index):
    balance = data_reader[email_index][2]
    print("Your Account Balance is "+balance)
    return balance

def deposit(data_reader, email_index):
    balance_input = float(input("Enter Your Deposit Amount: "))            
    balance = float(data_reader[email_index][2])
    new_balance = balance + balance_input
    data_reader[email_index][2] = new_balance
    with open("bank.csv","w") as fx:
        data_writer = csv.writer(fx)
        data_writer.writerows(data_reader)
    print("Your Deposit Amount is "+str(balance_input)+"\n")
    print("New Account Balance is "+str(new_balance))

def withdraw(data_reader, email_index):
    if data_reader[email_index][2] == "0.0":
        print("Your Account Balance is too low.Please make a deposit instead")
        deposit(data_reader, email_index)
    else:
        amount = float(input("enter amount to withdraw: "))
        balance = float(check_balance(data_reader, email_index))
        if amount > balance:
            print("\nInsufficient Funds\n")
        else:
            new_balance = balance - amount
            data_reader[email_index][2] = new_balance
            with open("bank.csv","w") as fx:
                data_writer = csv.writer(fx)
                data_writer.writerows(data_reader)
            print("\nAmount Withdrawn is "+str(amount)+"\n")
            print("New Account Balance is "+str(new_balance))

def transfer(data_reader, email_index):
    receiver_email = input("Enter the email you want to transfer to: ")
    emails = [i[0] for i in data_reader[1:] if i ]
    try:
        receiver_index = emails.index(receiver_email) + 1
    except ValueError:
        print("Email does not exist")
        transfer(data_reader, email_index)
    amount = float(input("Enter transfer amount: "))
    receiver_bal = float(data_reader[receiver_index][2])
    new_balance_receiver = receiver_bal + amount
    data_reader[receiver_index][2] = new_balance_receiver
    user_balance = float(data_reader[email_index][2])
    new_user_balance = user_balance - amount
    data_reader[email_index][2] = new_user_balance
    with open("bank.csv","w") as fx:
        data_writer = csv.writer(fx)
        data_writer.writerows(data_reader)
    print("Amount transferred "+str(amount)+"\n")
    print("New Account Balance is "+str(new_user_balance))

def transaction(email_index, data_reader):
    print("Press 1: check balance")
    print("Press 2: deposit") 
    print("Press 3: withdraw")
    print("Press 4: transfer")
    print("Press 9: Main Menu")
    print("Press 0: Exit App")
    transaction_input = input("")
    if transaction_input == "1":
        check_balance(data_reader, email_index)
        transaction(email_index, data_reader)
    if transaction_input == "2":
        deposit(data_reader, email_index)
        transaction(email_index, data_reader)
    if transaction_input == "3":
        withdraw(data_reader, email_index)
        transaction(email_index, data_reader)
    if transaction_input == "4":
        transfer(data_reader, email_index)
        transaction(email_index, data_reader)
    if transaction_input == "9":
    	init()
    if transaction_input == "0":
    	exit()

            
init()
    

