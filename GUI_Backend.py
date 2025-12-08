# bank_backend.py

import sqlite3
from datetime import date
import random
from classes_functions import CreditUnion, SavingsAccount, CheckingAccount, Account


def get_connection(db_path="credit_union.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS accounts ("
        "account_number INTEGER PRIMARY KEY AUTOINCREMENT,"
        "account_holder TEXT NOT NULL,"
        "balance REAL NOT NULL,"
        "account_type TEXT NOT NULL,"
        "interest_rate REAL,"
        "overdraft_limit REAL)"
    )

    # make sure last_interest_date column exists
    cursor.execute("PRAGMA table_info(accounts)")
    cols = [row[1] for row in cursor.fetchall()]
    if "last_interest_date" not in cols:
        cursor.execute("ALTER TABLE accounts ADD COLUMN last_interest_date TEXT")

    conn.commit()
    return conn


def init_credit_union(conn):
    cu = CreditUnion()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number, account_holder, balance, "
        "account_type, interest_rate, overdraft_limit FROM accounts"
    )
    rows = cursor.fetchall()

    for row in rows:
        acc_number = row[0]
        holder = row[1]
        balance = row[2]
        acc_type = row[3]
        interest = row[4]
        overdraft = row[5]

        if acc_type == "savings":
            if interest is None:
                interest = 0.01
            cu.open_account(
                "savings",
                acc_number,
                holder,
                balance=balance,
                interest_rate=interest
            )
        elif acc_type == "checking":
            if overdraft is None:
                overdraft = 0.0
            cu.open_account(
                "checking",
                acc_number,
                holder,
                balance=balance,
                overdraft_limit=overdraft
            )
        else:
            cu.accounts[acc_number] = Account(acc_number, holder, balance)

    return cu


def create_account_in_db_and_union(conn, cu, account_type,
                                   holder_name, initial_deposit,
                                   interest_rate=None, overdraft_limit=None):
    cursor = conn.cursor()

    if account_type == "savings":
        if interest_rate is None:
            interest_rate = 0.01
        acc_type_str = "savings"
        interest_value = interest_rate
        overdraft_value = 0.0
    elif account_type == "checking":
        if overdraft_limit is None:
            overdraft_limit = 0.0
        acc_type_str = "checking"
        interest_value = 0.0
        overdraft_value = overdraft_limit
    else:
        acc_type_str = "basic"
        interest_value = 0.0
        overdraft_value = 0.0

    cursor.execute(
        "INSERT INTO accounts (account_holder, balance, account_type, "
        "interest_rate, overdraft_limit, last_interest_date) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (holder_name, initial_deposit, acc_type_str,
         interest_value, overdraft_value, None)
    )
    conn.commit()
    account_number = cursor.lastrowid

    if account_type == "savings":
        cu.open_account(
            "savings",
            account_number,
            holder_name,
            balance=initial_deposit,
            interest_rate=interest_value
        )
    elif account_type == "checking":
        cu.open_account(
            "checking",
            account_number,
            holder_name,
            balance=initial_deposit,
            overdraft_limit=overdraft_value
        )
    else:
        cu.accounts[account_number] = Account(
            account_number,
            holder_name,
            initial_deposit
        )

    return cu.get_account(account_number)


def get_or_load_account(conn, cu, account_number):
    acc = cu.get_account(account_number)
    if acc is not None:
        return acc

    cursor = conn.cursor()
    cursor.execute(
        "SELECT account_number, account_holder, balance, "
        "account_type, interest_rate, overdraft_limit "
        "FROM accounts WHERE account_number = ?",
        (account_number,)
    )
    row = cursor.fetchone()
    if row is None:
        return None

    num = row[0]
    holder = row[1]
    balance = row[2]
    acc_type = row[3]
    interest = row[4]
    overdraft = row[5]

    if acc_type == "savings":
        if interest is None:
            interest = 0.01
        cu.open_account(
            "savings",
            num,
            holder,
            balance=balance,
            interest_rate=interest
        )
    elif acc_type == "checking":
        if overdraft is None:
            overdraft = 0.0
        cu.open_account(
            "checking",
            num,
            holder,
            balance=balance,
            overdraft_limit=overdraft
        )
    else:
        cu.accounts[num] = Account(num, holder, balance)

    return cu.get_account(num)


def update_account_in_db(conn, account):
    cursor = conn.cursor()

    if isinstance(account, SavingsAccount):
        acc_type = "savings"
        interest_value = account.interest_rate
        overdraft_value = 0.0
    elif isinstance(account, CheckingAccount):
        acc_type = "checking"
        interest_value = 0.0
        overdraft_value = account.overdraft_limit
    else:
        acc_type = "basic"
        interest_value = 0.0
        overdraft_value = 0.0

    cursor.execute(
        "UPDATE accounts SET balance = ?, account_type = ?, "
        "interest_rate = ?, overdraft_limit = ? "
        "WHERE account_number = ?",
        (account.balance, acc_type, interest_value,
         overdraft_value, account.account_number)
    )
    conn.commit()


def apply_accrued_interest(conn, cu, account_number):
    acc = get_or_load_account(conn, cu, account_number)
    if acc is None:
        return
    if not isinstance(acc, SavingsAccount):
        return

    cursor = conn.cursor()
    cursor.execute(
        "SELECT last_interest_date FROM accounts WHERE account_number = ?",
        (account_number,)
    )
    row = cursor.fetchone()
    today = date.today()
    today_str = today.isoformat()

    # if never set, just set it and return
    if row is None or row[0] is None:
        cursor.execute(
            "UPDATE accounts SET last_interest_date = ? WHERE account_number = ?",
            (today_str, account_number)
        )
        conn.commit()
        return

    try:
        last_date = date.fromisoformat(row[0])
    except:
        last_date = today

    days = (today - last_date).days
    if days <= 0:
        return

    # simple: apply account's own interest once per day
    i = 0
    while i < days:
        acc.apply_interest()
        i += 1

    update_account_in_db(conn, acc)
    cursor.execute(
        "UPDATE accounts SET last_interest_date = ? WHERE account_number = ?",
        (today_str, account_number)
    )
    conn.commit()
