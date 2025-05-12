import tkinter as tk
import random
from utils import database

class ScrollableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class CustomerGUI:
    def __init__(self, master, back_to_main=None):
        self.master = master
        self.master.geometry("600x500")
        self.master.title("FinSecure - Customer Dashboard")
        self.current_customer = None
        self.back_to_main = back_to_main
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)
        self.show_main_menu()
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.master, text="Welcome to FinSecure - Customer", font=("Segoe UI", 16, "bold")).pack(pady=10)
        tk.Button(self.master, text="Register", width=25, bg="#007acc", fg="white", command=self.register_screen).pack(pady=8)
        tk.Button(self.master, text="Login", width=25, bg="#4caf50", fg="white", command=self.login_screen).pack(pady=8)
        if self.back_to_main:
            tk.Button(self.master, text="⬅ Back to Main", width=25, bg="gray", fg="white", command=self.back_to_main).pack(pady=8)
        tk.Button(self.master, text="Exit", width=25, command=self.on_exit).pack(pady=20)

    def register_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Register New Customer", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.name_entry = self.create_input("Full Name")
        self.email_entry = self.create_input("Email")
        self.password_entry = self.create_input("Password", show="*")

        def submit():
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()

            if not name or not email or not password:
                self.status_label.config(text="❌ All fields are required.", fg="red")
                return

            cid = f"CUST{random.randint(1000,9999)}"
            balance = "0"
            try:
                database.save_customer({
                    "customer_id": cid,
                    "name": name,
                    "email": email,
                    "password": password,
                    "balance": balance
                })
                self.status_label.config(text=f"✅ Registered! Your ID is {cid}", fg="green")
            except ValueError as e:
                self.status_label.config(text=f"❌ {str(e)}", fg="red")

        tk.Button(self.master, text="Submit", command=submit, bg="#2196f3", fg="white").pack(pady=10)
        tk.Button(self.master, text="⬅ Back", command=self.show_main_menu, bg="gray", fg="white").pack()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Customer Login", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.login_id_entry = self.create_input("Customer ID")
        self.login_pw_entry = self.create_input("Password", show="*")

        def login():
            cid = self.login_id_entry.get()
            pw = self.login_pw_entry.get()
            customer = database.find_customer_by_id(cid)
            if customer and customer["password"] == pw:
                self.current_customer = customer
                self.dashboard()
            else:
                self.status_label.config(text="❌ Invalid credentials", fg="red")

        tk.Button(self.master, text="Login", command=login, bg="#4caf50", fg="white").pack(pady=10)
        tk.Button(self.master, text="⬅ Back", command=self.show_main_menu, bg="gray", fg="white").pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.current_customer['name']}", font=("Segoe UI", 14, "bold")).pack(pady=10)

        tk.Button(self.master, text="View Balance", command=self.view_balance, width=30).pack(pady=5)
        tk.Button(self.master, text="Deposit", command=lambda: self.transaction("Deposit"), width=30).pack(pady=5)
        tk.Button(self.master, text="Withdraw", command=lambda: self.transaction("Withdraw"), width=30).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.show_main_menu, width=30).pack(pady=20)

    def view_balance(self):
        self.status_label.config(text=f"💰 Your current balance is ${self.current_customer['balance']}", fg="blue")

    def transaction(self, txn_type):
        self.clear_window()
        tk.Label(self.master, text=f"{txn_type} Amount", font=("Segoe UI", 14, "bold")).pack(pady=10)

        amount_entry = tk.Entry(self.master)
        amount_entry.pack(pady=5)

        def process():
            try:
                amt = float(amount_entry.get())
                balance = float(self.current_customer['balance'])

                if txn_type == "Withdraw" and amt > balance:
                    self.status_label.config(text="❌ Insufficient funds.", fg="red")
                    return

                new_balance = balance + amt if txn_type == "Deposit" else balance - amt
                database.update_customer_balance(self.current_customer['customer_id'], new_balance)
                database.log_transaction(
                    self.current_customer['customer_id'],
                    self.current_customer['name'],
                    txn_type,
                    amt,
                    new_balance
                )
                self.current_customer['balance'] = str(new_balance)
                self.status_label.config(
                    text=f"✅ {txn_type} of ${amt:.2f} successful. New balance: ${new_balance:.2f}", fg="green"
                )
                self.dashboard()
            except:
                self.status_label.config(text="❌ Invalid input.", fg="red")

        tk.Button(self.master, text="Submit", command=process, bg="#007acc", fg="white").pack(pady=5)
        tk.Button(self.master, text="⬅ Back", command=self.dashboard, bg="gray", fg="white").pack()

    def create_input(self, label, show=None):
        tk.Label(self.master, text=label, font=("Segoe UI", 10)).pack()
        entry = tk.Entry(self.master, show=show)
        entry.pack()
        return entry

    def on_exit(self):
        database.persist_customers_to_csv()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerGUI(root)
    root.mainloop()
