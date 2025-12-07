# bank_gui.py

import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import GUI_Backend as backend


class BankApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Default font: Times New Roman
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Times New Roman", size=12)
        self.option_add("*Font", default_font)
        self.option_add("*Label.Font", default_font)
        self.option_add("*Button.Font", default_font)
        self.option_add("*Entry.Font", default_font)
        self.option_add("*Radiobutton.Font", default_font)

        self.title("Credit Union System")
        self.geometry("520x400")

        self.conn = backend.get_connection()
        self.credit_union = backend.init_credit_union(self.conn)

        self.current_account_number = None

        self.login_frame = None
        self.create_frame = None
        self.account_frame = None

        self.create_login_frame()
        self.create_create_frame()
        self.create_account_frame()

        self.show_login_frame()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # ----------------- Frame creation -----------------

    def create_login_frame(self):
        self.login_frame = tk.Frame(self)

        title = tk.Label(self.login_frame,
                         text="Welcome to the Credit Union",
                         font=("Times New Roman", 16))
        title.pack(pady=10)

        tk.Label(self.login_frame, text="Account Number:").pack()
        self.entry_login_number = tk.Entry(self.login_frame)
        self.entry_login_number.pack(pady=5)

        tk.Button(self.login_frame, text="Login", command=self.login).pack(pady=5)

        tk.Label(self.login_frame, text="-----------------------------").pack(pady=10)

        tk.Button(self.login_frame, text="Create New Account",
                  command=self.show_create_frame).pack(pady=5)

    def create_create_frame(self):
        self.create_frame = tk.Frame(self)

        title = tk.Label(self.create_frame,
                         text="Open New Account",
                         font=("Times New Roman", 16))
        title.pack(pady=10)

        tk.Label(self.create_frame, text="Account Holder Name:").pack()
        self.entry_holder_name = tk.Entry(self.create_frame)
        self.entry_holder_name.pack(pady=5)

        tk.Label(self.create_frame, text="Initial Deposit:").pack()
        self.entry_initial_deposit = tk.Entry(self.create_frame)
        self.entry_initial_deposit.pack(pady=5)

        tk.Label(self.create_frame, text="Account Type:").pack(pady=5)

        self.account_type_var = tk.StringVar()
        self.account_type_var.set("savings")

        tk.Radiobutton(
            self.create_frame,
            text="Savings Account",
            variable=self.account_type_var,
            value="savings"
        ).pack()

        tk.Radiobutton(
            self.create_frame,
            text="Checking Account",
            variable=self.account_type_var,
            value="checking"
        ).pack()

        self.label_interest = tk.Label(self.create_frame,
                                       text="Interest Rate (for Savings):")
        self.label_interest.pack(pady=5)
        self.entry_interest = tk.Entry(self.create_frame)
        self.entry_interest.insert(0, "0.01")
        self.entry_interest.pack(pady=5)

        self.label_overdraft = tk.Label(self.create_frame,
                                        text="Overdraft Limit (for Checking):")
        self.label_overdraft.pack(pady=5)
        self.entry_overdraft = tk.Entry(self.create_frame)
        self.entry_overdraft.insert(0, "0.00")
        self.entry_overdraft.pack(pady=5)

        tk.Button(self.create_frame, text="Create Account",
                  command=self.create_account).pack(pady=5)
        tk.Button(self.create_frame, text="Back to Login",
                  command=self.show_login_frame).pack(pady=5)

    def create_account_frame(self):
        self.account_frame = tk.Frame(self)

        tk.Label(self.account_frame,
                 text="Your Account",
                 font=("Times New Roman", 16)).pack(pady=10)

        self.label_acc_number = tk.Label(self.account_frame, text="Account Number: -")
        self.label_acc_number.pack()

        self.label_acc_holder = tk.Label(self.account_frame, text="Holder: -")
        self.label_acc_holder.pack()

        self.label_acc_type = tk.Label(self.account_frame, text="Type: -")
        self.label_acc_type.pack()

        self.label_acc_balance = tk.Label(self.account_frame, text="Balance: $0.00")
        self.label_acc_balance.pack(pady=5)

        tk.Label(self.account_frame, text="Amount:").pack()
        self.entry_amount = tk.Entry(self.account_frame)
        self.entry_amount.pack(pady=5)

        tk.Button(self.account_frame, text="Deposit",
                  command=self.deposit).pack(pady=3)
        tk.Button(self.account_frame, text="Withdraw",
                  command=self.withdraw).pack(pady=3)

        tk.Button(self.account_frame, text="Logout",
                  command=self.show_login_frame).pack(pady=10)

    # ----------------- Frame switching -----------------

    def hide_all_frames(self):
        self.login_frame.pack_forget()
        self.create_frame.pack_forget()
        self.account_frame.pack_forget()

    def show_login_frame(self):
        self.hide_all_frames()
        self.entry_login_number.delete(0, tk.END)
        self.login_frame.pack(fill="both", expand=True)

    def show_create_frame(self):
        self.hide_all_frames()
        self.entry_holder_name.delete(0, tk.END)
        self.entry_initial_deposit.delete(0, tk.END)
        self.entry_interest.delete(0, tk.END)
        self.entry_interest.insert(0, "0.01")
        self.entry_overdraft.delete(0, tk.END)
        self.entry_overdraft.insert(0, "0.00")
        self.create_frame.pack(fill="both", expand=True)

    def show_account_frame(self):
        self.hide_all_frames()
        self.update_account_labels()
        self.account_frame.pack(fill="both", expand=True)

    # ----------------- Logic -----------------

    def login(self):
        text = self.entry_login_number.get().strip()
        if text == "":
            messagebox.showerror("Error", "Please enter your account number.")
            return

        try:
            acc_number = int(text)
        except:
            messagebox.showerror("Error", "Account number must be a number.")
            return

        acc = backend.get_or_load_account(self.conn, self.credit_union, acc_number)
        if acc is None:
            messagebox.showerror("Error", "Account not found.")
            return

        # apply any daily interest (for savings)
        backend.apply_accrued_interest(self.conn, self.credit_union, acc_number)

        self.current_account_number = acc_number
        self.show_account_frame()

    def create_account(self):
        name = self.entry_holder_name.get().strip()
        deposit_text = self.entry_initial_deposit.get().strip()
        acc_type = self.account_type_var.get()

        if name == "":
            messagebox.showerror("Error", "Account holder name is required.")
            return

        if deposit_text == "":
            initial = 0.0
        else:
            try:
                initial = float(deposit_text)
            except:
                messagebox.showerror("Error", "Initial deposit must be a number.")
                return

            if initial < 0:
                messagebox.showerror("Error", "Initial deposit cannot be negative.")
                return

        interest_rate = None
        overdraft_limit = None

        if acc_type == "savings":
            interest_text = self.entry_interest.get().strip()
            if interest_text == "":
                interest_rate = 0.01
            else:
                try:
                    interest_rate = float(interest_text)
                except:
                    messagebox.showerror("Error", "Interest rate must be a number.")
                    return
        else:
            overdraft_text = self.entry_overdraft.get().strip()
            if overdraft_text == "":
                overdraft_limit = 0.0
            else:
                try:
                    overdraft_limit = float(overdraft_text)
                except:
                    messagebox.showerror("Error", "Overdraft limit must be a number.")
                    return

        acc = backend.create_account_in_db_and_union(
            self.conn,
            self.credit_union,
            acc_type,
            name,
            initial,
            interest_rate=interest_rate,
            overdraft_limit=overdraft_limit
        )

        self.current_account_number = acc.account_number

        messagebox.showinfo(
            "Account Created",
            "Account created successfully.\nYour account number is: " + str(acc.account_number)
        )

        self.show_account_frame()

    def get_current_account(self):
        if self.current_account_number is None:
            return None
        return self.credit_union.get_account(self.current_account_number)

    def update_account_labels(self):
        acc = self.get_current_account()
        if acc is None:
            self.label_acc_number.config(text="Account Number: -")
            self.label_acc_holder.config(text="Holder: -")
            self.label_acc_type.config(text="Type: -")
            self.label_acc_balance.config(text="Balance: $0.00")
            return

        class_name = acc.__class__.__name__
        if class_name == "SavingsAccount":
            type_text = "Savings"
        elif class_name == "CheckingAccount":
            type_text = "Checking"
        else:
            type_text = "Account"

        self.label_acc_number.config(text="Account Number: " + str(acc.account_number))
        self.label_acc_holder.config(text="Holder: " + str(acc.account_holder))
        self.label_acc_type.config(text="Type: " + type_text)
        self.label_acc_balance.config(
            text="Balance: $" + "{:.2f}".format(acc.balance)
        )

    def deposit(self):
        acc = self.get_current_account()
        if acc is None:
            messagebox.showerror("Error", "No account is loaded.")
            return

        text = self.entry_amount.get().strip()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Deposit amount must be positive.")
            return

        ok = self.credit_union.deposit(self.current_account_number, amount)
        if not ok:
            messagebox.showerror("Error", "Deposit failed.")
            return

        backend.update_account_in_db(self.conn, acc)
        self.entry_amount.delete(0, tk.END)
        self.update_account_labels()
        messagebox.showinfo("Deposit", "Deposit successful.")

    def withdraw(self):
        acc = self.get_current_account()
        if acc is None:
            messagebox.showerror("Error", "No account is loaded.")
            return

        text = self.entry_amount.get().strip()
        if text == "":
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(text)
        except:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        ok = self.credit_union.withdraw(self.current_account_number, amount)
        if not ok:
            messagebox.showerror("Error", "Withdrawal failed. Check balance or overdraft limit.")
            return

        backend.update_account_in_db(self.conn, acc)
        self.entry_amount.delete(0, tk.END)
        self.update_account_labels()
        messagebox.showinfo("Withdraw", "Withdrawal successful.")

    def on_close(self):
        try:
            self.conn.close()
        except:
            pass
        self.destroy()


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()
