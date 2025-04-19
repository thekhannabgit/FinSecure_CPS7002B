# GUI/GUICustomer.py
import tkinter as tk
from tkinter import messagebox
import random
from utils import database

class CustomerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FinSecure - Customer Portal")
        self.current_customer = None
        self.show_main_menu()
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.master, text="Welcome to FinSecure - Customer", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.master, text="Register", width=20, command=self.register_screen).pack(pady=5)
        tk.Button(self.master, text="Login", width=20, command=self.login_screen).pack(pady=5)

    def register_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Register New Customer", font=("Arial", 14)).pack(pady=10)

        self.name_entry = self.create_input("Full Name")
        self.email_entry = self.create_input("Email")
        self.password_entry = self.create_input("Password", show="*")

        def submit():
            cid = f"CUST{random.randint(1000,9999)}"
            name = self.name_entry.get()
            email = self.email_entry.get()
            password = self.password_entry.get()
            balance = "0"
            try:
                database.save_customer({
                    "customer_id": cid,
                    "name": name,
                    "email": email,
                    "password": password,
                    "balance": balance
                })
                messagebox.showinfo("Success", f"Registered! Your ID is {cid}")
                self.show_main_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.master, text="Submit", command=submit).pack(pady=10)
        tk.Button(self.master, text="Back", command=self.show_main_menu).pack()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Customer Login", font=("Arial", 14)).pack(pady=10)

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
                messagebox.showerror("Error", "Invalid credentials.")

        tk.Button(self.master, text="Login", command=login).pack(pady=10)
        tk.Button(self.master, text="Back", command=self.show_main_menu).pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.current_customer['name']}", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.master, text="View Balance", command=self.view_balance).pack(pady=5)
        tk.Button(self.master, text="Deposit", command=lambda: self.transaction("Deposit")).pack(pady=5)
        tk.Button(self.master, text="Withdraw", command=lambda: self.transaction("Withdraw")).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.show_main_menu).pack(pady=10)

    def view_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is ${self.current_customer['balance']}")

    def transaction(self, txn_type):
        self.clear_window()
        tk.Label(self.master, text=f"{txn_type} Amount", font=("Arial", 14)).pack(pady=10)

        amount_entry = tk.Entry(self.master)
        amount_entry.pack(pady=5)

        def process():
            try:
                amt = float(amount_entry.get())
                balance = float(self.current_customer['balance'])
                if txn_type == "Withdraw" and amt > balance:
                    messagebox.showerror("Error", "Insufficient funds.")
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
                messagebox.showinfo("Success", f"{txn_type} complete. New balance: ${new_balance}")
                self.dashboard()
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(self.master, text="Submit", command=process).pack(pady=5)
        tk.Button(self.master, text="Back", command=self.dashboard).pack()

    def create_input(self, label, show=None):
        tk.Label(self.master, text=label).pack()
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
