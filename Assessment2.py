from pywebio.input import *
from pywebio.output import *
from pywebio import start_server
from datetime import datetime
from pywebio.output import put_markdown
from pywebio.output import put_image

balance=100
users = {'Clinton': 'abc1234'}
transactions= ["-£30     Aldi         20/03/2025", "+£20     Carl         10/03/2025", "-£40     BT           01/03/2025", "-£50     Mandy        25/02/2025", "-£20     Sam          20/02/2025", "-£14     Tom          17/02/2025", "+£200    DC LTD       10/02/2025" ]
transaction_update=[]
payees={
    "Patrick":{"Bank": "Barclays", "Account number":"12034", "Sort Code":"123"},
    "Mandy":{"Bank": "Aviro", "Account number":"30432", "Sort Code":"453"},
    "Sam":{"Bank": "HPLTD", "Account number":"66119", "Sort Code":"200"},
    "Tom":{"Bank": "Barclays", "Account number":"30444", "Sort Code":"359"}
}
selected_payee=None

def user_login():
    #Starting page of the App
    clear()
    put_html("<h1>Login</h1>")
    #button that is clicked if the user forget their login credentials
    put_buttons(['Forgot password?'], onclick=[user_password_reset])
    #Input field that asks the user to input their login credentials
    data = input_group('', [
        input("Username:", name="name", required=True),
        input("Password:", name="password", required=True, type=PASSWORD),
    ])


    username = data['name']
    password = data['password']
    #validations in place to determine if the user is going to login
    if username in users and users[username] == password:
        home(username)  # Go to dashboard
    else:
        toast("Incorrect username or password")
        user_login()  # Retry login after failure

def home(user):
    #home page
    clear()
    put_html(f"<h1>Accounts</h1>")
    #Asks the user to select the account to be used to perform transaction
    put_html(f"<p1>Please select an account to proceed:</p1>")
    put_buttons(['Account 1'], onclick=[account_summary])
    put_buttons(['Products'], onclick=[products])
    put_buttons(['Log out'], onclick=[user_logout])

def account_summary():
    #Account operation option page
    clear()
    put_html("<h1>Account Summary</h1>")
    #Displays the available balance within the selected account
    put_markdown(f"> **|Current balance: £{balance}**|")
    #Button that send the user to the select payee page
    put_buttons(['Move money'], onclick=[select_payee])
    #Displays transactions history
    put_html("<h2>Transactions</h2>")
    for transaction in transactions:
        put_markdown(f">{transaction}")
    put_buttons(['Back', 'Log out'], onclick=[lambda: home("Clinton"),user_logout])


def select_payee():
    #select payee page
    global selected_payee
    clear()
    #Asks user to select payee they want to send money to
    put_html("<h1>Select Payee</h1>")
    payees_options=[name for name in payees.keys()]
    #It shows that when a payee is selected the user is going to be sent to the enter amount page
    def payee_choice(name):
        global selected_payee
        selected_payee=name
        enter_amount()

    put_buttons(payees_options, onclick=payee_choice )
    #Button that allow the user to add new payees
    put_buttons(["+"], onclick=[add_payee])
    put_buttons(['Log out', 'Back'], onclick=[user_logout, account_summary])

def add_payee():
    #Add payee page
    clear()
    put_html("<h1>Add new Payees</h1>")
    #Input field that the user is going to use to enter the information of the payee that they want to add
    while True:
        data = input_group('', [
            input("Payee name:", name="name", required=True),
            input("Bank:", name="bank", required=True),
            input("Account Number", name="account_number", required=True),
            input("Sort Code", name="sort_code", required=True)
        ])
        account_number=str(data["account_number"])
        sort_code=str(data["sort_code"])
    #Input validation of some of the input fields
        if len(account_number) !=5:
            toast("Account number has to be 5 numbers")
            return add_payee()
        elif len(sort_code)!=3:
            toast("Sort code has to be 3 numbers")
            return add_payee()
        else:
            break

    #It shows how the payee is going to be added to the already existing payee list
    payees[data["name"]] = {
        "bank": data["bank"],
        "account_number": account_number,
        "sort_code": sort_code
    }

    toast("Payee added successfully!")
    select_payee()

def enter_amount():
    #Enter amount page
    global balance, selected_payee
    clear()
    put_html("<h1>Enter amount</h1>")
    #Input field for the user to enter the amount they want to send
    input_amount=int(input("Enter amount £:"))
    put_buttons(['Back'], onclick=[select_payee])
    #Input validations in place for the amount
    if input_amount > balance:
        toast("Not enough balance for transaction")
        enter_amount()
    elif input_amount==0:
        toast("Invalid balance input")
        enter_amount()
    else:
        balance-=input_amount
        now= datetime.now().strftime("%d/%m/%y")
        #It shows how the transaction history is going to get updated after a successful transaction
        transactions.insert(0, f"-£{input_amount} {selected_payee} {now}")
        toast("Payment has been successful")
        payment_successful()

def payment_successful():
    #Successfull payment page
    clear()
    put_html("<h1>Payment successful</h1>")
    put_buttons(['Close'], onclick=[lambda: home("Clinton")])

def user_logout():
    #Logs out the user from the application
    clear()
    user_login()


def user_password_reset():
    #Password reset page
    clear()
    put_html("<h1>Password Reset</h1>")
    put_buttons(['Back'], onclick=[user_login])
    #Input field for the use to enter their username
    while True:
        username = input("Enter username:", required=True)
    #it shows what happens if username is incorrect
        if username not in users:
            toast("Username not found")
        else:
            break
    #if the username is correct it will display an input field for the user to input the new password
    while True:
        data_password = input_group("Reset Password", [
            input("New Password:", name="new_password", required=True, type=PASSWORD),
            input("Confirm Password:", name="confirm_password", required=True, type=PASSWORD)
        ])
        if data_password['new_password'] !=data_password['confirm_password']:
            toast("The passwords don't match!")
        else:
            break
    #end of the password reset process
    users[username] = data_password['new_password']
    toast("Password has been updated!")
    clear()
    put_html("<h2>Password updated successfully! Please log in.</h2>")

def products():
    #products page
    clear()
    put_html("<h1>Products</h1>")
    #Buttons that allow the user to access additional options within the banking app
    put_buttons(['Loans'], onclick=[loans])
    put_buttons(['Mortgages'], onclick=[mortgages])
    put_buttons(['Credit cards'], onclick=[credit_cards])
    put_buttons(['Back', 'Logout'], onclick=[lambda:home('Clinton'), user_logout])


def loans():
    #loans page
    clear()
    put_html("<h1>Loans</h1>")
    put_html("<p1>Our personal loans are just for our current account members. You can apply for a loan of between £1,000 and £50,000 over"
             "1 to 7 years. Conditions apply.6.1% APR Representative (fixed) on loans of between £7,500 and £25,000 over 1 to 5 years.</p1>")
    put_html("<p1>To apply visit:  https://www.nationwide.co.uk/loans/apply/</p1>")
    put_buttons(['Back', 'Logout'], onclick=[products, user_logout])

def mortgages():
    #mortgages page
    clear()
    put_html("<h1>Mortgages</h1>")
    put_html("<p1>Whether you’re a first time buyer or looking for a better deal, we can help you find a mortgage that’s right for you."
             "for more info visit:  https://www.nationwide.co.uk/mortgages/</p1>")
    put_buttons(['Back', 'Logout'], onclick=[products, user_logout])

def credit_cards():
    #credit cards page
    clear()
    put_html("<h1>Credit cards</h1>")
    put_html("<p1>Our Member Credit Card has 2 great introductory offers to choose from. Available if you have a savings account, current account or mortgage with us."
             "for more info visit  :https://www.nationwide.co.uk/credit-cards/</p1>")
    put_buttons(['Back', 'Logout'], onclick=[products, user_logout])

if __name__ == '__main__':
    start_server(user_login, port=500, debug=True)