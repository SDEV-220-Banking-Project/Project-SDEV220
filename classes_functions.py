'''This will be for a local credit union system
that allows workers to open new checking and savings accounts
and search for existing accounts as well as 
perform deposits and withdrawals.'''

# Person class to represent account holders
class Person:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone
    # String representation of the Person
    def __str__(self):
        return f'Person({self.name}, {self.address}, {self.phone})'

# Base Account class
class Account:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
    # Method to deposit money into the account
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False
    # Method to withdraw money from the account
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False
    # Method to get the current balance
    def get_balance(self):
        return self.balance
    # String representation of the Account
    def __str__(self):
        return f'Account({self.account_number}, {self.account_holder}, Balance: {self.balance})'

# Savings Account subclass of Account
class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, balance=0, interest_rate=0.01):
        super().__init__(account_number, account_holder, balance)
        self.interest_rate = interest_rate
    # Method to apply interest to the savings account
    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest)
    # String representation of the SavingsAccount
    def __str__(self):
        return f'SavingsAccount({self.account_number}, {self.account_holder}, Balance: {self.balance}, Interest Rate: {self.interest_rate})'

# Checking Account subclass of Account
class CheckingAccount(Account):
    def __init__(self, account_number, account_holder, balance=0, overdraft_limit=0):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = overdraft_limit

    # Method to withdraw money from the checking account with overdraft limit
    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            return True
        return False
    
    # Method to deposit money into the checking account
    def deposit(self, amount):
        return super().deposit(amount)
    
    # String representation of the CheckingAccount
    def __str__(self):
        return f'CheckingAccount({self.account_number}, {self.account_holder}, Balance: {self.balance}, Overdraft Limit: {self.overdraft_limit})'

# CreditUnion class to manage multiple accounts
class CreditUnion:
    # Initialize the CreditUnion with an empty account list
    def __init__(self):
        self.accounts = {}

    # Method to open a new account
    def open_account(self, account_type, account_number, account_holder, **kwargs):
        if account_number in self.accounts:
            return False  # Account already exists
        if account_type == 'savings':
            account = SavingsAccount(account_number, account_holder, **kwargs)
        elif account_type == 'checking':
            account = CheckingAccount(account_number, account_holder, **kwargs)
        else:
            return False  # Invalid account type
        self.accounts[account_number] = account
        return True

    # Method to get an account by account number
    def get_account(self, account_number):
        return self.accounts.get(account_number, None)

    # Method to deposit money into an account by account number
    def deposit(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            return account.deposit(amount)
        return False

    # Method to withdraw money from an account by account number
    def withdraw(self, account_number, amount):
        account = self.get_account(account_number)
        if account:
            return account.withdraw(amount)
        return False
    
    # Method to display all accounts
    def display_accounts(self):
        if not self.accounts:
            return "No accounts available."
        else:
            for account in self.accounts.values():
                print(account)

    # String representation of the CreditUnion    
    def __str__(self):
        return f'CreditUnion(Accounts: {len(self.accounts)})'

