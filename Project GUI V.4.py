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
        
        # Set dark blue background
        self.login_frame.configure(bg="#0a1e3d")
        
        # Create widgets first
        self.entry_login_number = tk.Entry(self.login_frame, width=25)
        self.login_btn = tk.Button(self.login_frame, 
                             text="Login", 
                             command=self.login,
                             bg="#1e4d7b",
                             fg="white",
                             width=20)
        self.create_btn = tk.Button(self.login_frame, 
                              text="Create New Account",
                              command=self.show_create_frame,
                              bg="#1e4d7b",
                              fg="white",
                              width=20)
        
        # Create canvas for background
        self.bg_canvas = tk.Canvas(self.login_frame, highlightthickness=0, bd=0, bg="#0a1e3d")
        self.bg_canvas.pack(fill="both", expand=True)
        
        self.bg_canvas.bind('<Configure>', self._on_canvas_configure)
        
    def _on_canvas_configure(self, event):
        if hasattr(self, '_last_canvas_size'):
            if abs(event.width - self._last_canvas_size[0]) < 5 and abs(event.height - self._last_canvas_size[1]) < 5:
                return
        self._last_canvas_size = (event.width, event.height)
        
        self.bg_canvas.delete("all")
        
        canvas_width = event.width
        canvas_height = event.height
        
        # Try to load background image
        try:
            if not hasattr(self, 'bg_photo'):
                self.bg_photo = tk.PhotoImage(file="CyberBackground.PNG")
            self.bg_canvas.create_image(canvas_width//2, canvas_height//2, image=self.bg_photo)
        except Exception as e:
            pass  # If image fails, just use the blue background
        
        center_x = canvas_width // 2
        
        logo_y_position = int(canvas_height * 0.15)
        
        # Load MMNT logo
        try:
            if not hasattr(self, 'logo_photo'):
                self.logo_photo = tk.PhotoImage(file="MMNTLogo1.png")
            self.bg_canvas.create_image(center_x, logo_y_position, image=self.logo_photo)
        except:
            # If logo fails, show text
            self.bg_canvas.create_text(center_x, logo_y_position,
                                 text="MMNT Banking",
                                 font=("Arial", 24, "bold"),
                                 fill="white")
        
        y_start = int(canvas_height * 0.50)
        
        # Welcome text
        self.bg_canvas.create_text(center_x, y_start,
                             text="Welcome to the Credit Union",
                             font=("Times New Roman", 16),
                             fill="white")
        y_start += 40
        
        # Account Number label
        self.bg_canvas.create_text(center_x, y_start,
                             text="Account Number:",
                             font=("Times New Roman", 12),
                             fill="white")
        y_start += 30
        
        # Entry widget
        entry_window = self.bg_canvas.create_window(center_x, y_start, window=self.entry_login_number)
        self.bg_canvas.tag_raise(entry_window)
        y_start += 35
        
        # Login button
        login_window = self.bg_canvas.create_window(center_x, y_start, window=self.login_btn)
        self.bg_canvas.tag_raise(login_window)
        y_start += 40
        
        # Separator
        self.bg_canvas.create_text(center_x, y_start,
                             text="-----------------------------",
                             font=("Times New Roman", 12),
                             fill="white")
        y_start += 30
        
        # Create New Account button
        create_window = self.bg_canvas.create_window(center_x, y_start, window=self.create_btn)
        self.bg_canvas.tag_raise(create_window)
        
        self.entry_login_number.lift()
        self.login_btn.lift()
        self.create_btn.lift()

    def create_create_frame(self):
        self.create_frame = tk.Frame(self)
        self.create_frame.configure(bg="#0a1e3d")
        
        # Create all widgets first
        self.entry_holder_name = tk.Entry(self.create_frame, width=25)
        self.entry_initial_deposit = tk.Entry(self.create_frame, width=25)
        self.entry_interest = tk.Entry(self.create_frame, width=25)
        self.entry_overdraft = tk.Entry(self.create_frame, width=25)
        
        self.account_type_var = tk.StringVar()
        self.account_type_var.set("savings")
        
        self.radio_savings = tk.Radiobutton(
            self.create_frame,
            text="Savings Account",
            variable=self.account_type_var,
            value="savings",
            bg="#0a1e3d",
            fg="white",
            selectcolor="#1e4d7b"
        )
        
        self.radio_checking = tk.Radiobutton(
            self.create_frame,
            text="Checking Account",
            variable=self.account_type_var,
            value="checking",
            bg="#0a1e3d",
            fg="white",
            selectcolor="#1e4d7b"
        )
        
        self.btn_create = tk.Button(self.create_frame, 
                                     text="Create Account",
                                     command=self.create_account,
                                     bg="#1e4d7b",
                                     fg="white",
                                     width=20)
        
        self.btn_back = tk.Button(self.create_frame, 
                                  text="Back to Login",
                                  command=self.show_login_frame,
                                  bg="#1e4d7b",
                                  fg="white",
                                  width=20)
        
        # Create canvas for background
        self.create_canvas = tk.Canvas(self.create_frame, highlightthickness=0, bd=0, bg="#0a1e3d")
        self.create_canvas.pack(fill="both", expand=True)
        
        self.create_canvas.bind('<Configure>', self._on_create_canvas_configure)
    
    def _on_create_canvas_configure(self, event):
        if hasattr(self, '_last_create_canvas_size'):
            if abs(event.width - self._last_create_canvas_size[0]) < 5 and abs(event.height - self._last_create_canvas_size[1]) < 5:
                return
        self._last_create_canvas_size = (event.width, event.height)
        
        self.create_canvas.delete("all")
        
        canvas_width = event.width
        canvas_height = event.height
        
        # Try to load background image
        try:
            if not hasattr(self, 'bg_photo'):
                self.bg_photo = tk.PhotoImage(file="CyberBackground.PNG")
            self.create_canvas.create_image(canvas_width//2, canvas_height//2, image=self.bg_photo)
        except:
            pass
        
        center_x = canvas_width // 2
        y_start = 30
        
        # Title
        self.create_canvas.create_text(center_x, y_start,
                                       text="Open New Account",
                                       font=("Times New Roman", 16),
                                       fill="white")
        y_start += 40
        
        # Account Holder Name
        self.create_canvas.create_text(center_x, y_start,
                                       text="Account Holder Name:",
                                       font=("Times New Roman", 12),
                                       fill="white")
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.entry_holder_name)
        y_start += 30
        
        # Initial Deposit
        self.create_canvas.create_text(center_x, y_start,
                                       text="Initial Deposit:",
                                       font=("Times New Roman", 12),
                                       fill="white")
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.entry_initial_deposit)
        y_start += 35
        
        # Account Type
        self.create_canvas.create_text(center_x, y_start,
                                       text="Account Type:",
                                       font=("Times New Roman", 12),
                                       fill="white")
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.radio_savings)
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.radio_checking)
        y_start += 35
        
        # Interest Rate
        self.create_canvas.create_text(center_x, y_start,
                                       text="Interest Rate (for Savings):",
                                       font=("Times New Roman", 12),
                                       fill="white")
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.entry_interest)
        y_start += 30
        
        # Overdraft Limit
        self.create_canvas.create_text(center_x, y_start,
                                       text="Overdraft Limit (for Checking):",
                                       font=("Times New Roman", 12),
                                       fill="white")
        y_start += 25
        self.create_canvas.create_window(center_x, y_start, window=self.entry_overdraft)
        y_start += 35
        
        # Buttons
        create_win = self.create_canvas.create_window(center_x, y_start, window=self.btn_create)
        self.create_canvas.tag_raise(create_win)
        y_start += 35
        back_win = self.create_canvas.create_window(center_x, y_start, window=self.btn_back)
        self.create_canvas.tag_raise(back_win)
        
        # Lift all widgets to front
        self.entry_holder_name.lift()
        self.entry_initial_deposit.lift()
        self.entry_interest.lift()
        self.entry_overdraft.lift()
        self.radio_savings.lift()
        self.radio_checking.lift()
        self.btn_create.lift()
        self.btn_back.lift()

    def create_account_frame(self):
        self.account_frame = tk.Frame(self)
        self.account_frame.configure(bg="#0a1e3d")
        
        # Create all widgets first
        self.label_acc_number = tk.Label(self.account_frame, text="Account Number: -",
                                         fg="white", bg="#0a1e3d", font=("Times New Roman", 12))
        self.label_acc_holder = tk.Label(self.account_frame, text="Holder: -",
                                         fg="white", bg="#0a1e3d", font=("Times New Roman", 12))
        self.label_acc_type = tk.Label(self.account_frame, text="Type: -",
                                       fg="white", bg="#0a1e3d", font=("Times New Roman", 12))
        self.label_acc_balance = tk.Label(self.account_frame, text="Balance: $0.00",
                                          fg="white", bg="#0a1e3d", font=("Times New Roman", 12))
        
        self.entry_amount = tk.Entry(self.account_frame, width=25)
        
        self.btn_deposit = tk.Button(self.account_frame, text="Deposit",
                                     command=self.deposit,
                                     bg="#1e4d7b",
                                     fg="white",
                                     width=20)
        
        self.btn_withdraw = tk.Button(self.account_frame, text="Withdraw",
                                      command=self.withdraw,
                                      bg="#1e4d7b",
                                      fg="white",
                                      width=20)
        
        self.btn_logout = tk.Button(self.account_frame, text="Logout",
                                    command=self.show_login_frame,
                                    bg="#1e4d7b",
                                    fg="white",
                                    width=20)
        
        # Create canvas for background
        self.account_canvas = tk.Canvas(self.account_frame, highlightthickness=0, bd=0, bg="#0a1e3d")
        self.account_canvas.pack(fill="both", expand=True)
        
        self.account_canvas.bind('<Configure>', self._on_account_canvas_configure)
    
    def _on_account_canvas_configure(self, event):
        if hasattr(self, '_last_account_canvas_size'):
            if abs(event.width - self._last_account_canvas_size[0]) < 5 and abs(event.height - self._last_account_canvas_size[1]) < 5:
                return
        self._last_account_canvas_size = (event.width, event.height)
        
        self.account_canvas.delete("all")
        
        canvas_width = event.width
        canvas_height = event.height
        
        # Try to load background image
        try:
            if not hasattr(self, 'bg_photo'):
                self.bg_photo = tk.PhotoImage(file="CyberBackground.PNG")
            self.account_canvas.create_image(canvas_width//2, canvas_height//2, image=self.bg_photo)
        except:
            pass
        
        center_x = canvas_width // 2
        y_start = 30
        
        # Title
        self.account_canvas.create_text(center_x, y_start,
                                        text="Your Account",
                                        font=("Times New Roman", 16),
                                        fill="white")
        y_start += 40
        
        # Account info labels
        acc_num_win = self.account_canvas.create_window(center_x, y_start, window=self.label_acc_number)
        self.account_canvas.tag_raise(acc_num_win)
        y_start += 25
        
        holder_win = self.account_canvas.create_window(center_x, y_start, window=self.label_acc_holder)
        self.account_canvas.tag_raise(holder_win)
        y_start += 25
        
        type_win = self.account_canvas.create_window(center_x, y_start, window=self.label_acc_type)
        self.account_canvas.tag_raise(type_win)
        y_start += 25
        
        balance_win = self.account_canvas.create_window(center_x, y_start, window=self.label_acc_balance)
        self.account_canvas.tag_raise(balance_win)
        y_start += 40
        
        # Amount label
        self.account_canvas.create_text(center_x, y_start,
                                        text="Amount:",
                                        font=("Times New Roman", 12),
                                        fill="white")
        y_start += 25
        
        # Amount entry
        amount_win = self.account_canvas.create_window(center_x, y_start, window=self.entry_amount)
        self.account_canvas.tag_raise(amount_win)
        y_start += 35
        
        # Deposit button
        deposit_win = self.account_canvas.create_window(center_x, y_start, window=self.btn_deposit)
        self.account_canvas.tag_raise(deposit_win)
        y_start += 35
        
        # Withdraw button
        withdraw_win = self.account_canvas.create_window(center_x, y_start, window=self.btn_withdraw)
        self.account_canvas.tag_raise(withdraw_win)
        y_start += 45
        
        # Logout button
        logout_win = self.account_canvas.create_window(center_x, y_start, window=self.btn_logout)
        self.account_canvas.tag_raise(logout_win)
        
        # Lift all widgets
        self.label_acc_number.lift()
        self.label_acc_holder.lift()
        self.label_acc_type.lift()
        self.label_acc_balance.lift()
        self.entry_amount.lift()
        self.btn_deposit.lift()
        self.btn_withdraw.lift()
        self.btn_logout.lift()

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