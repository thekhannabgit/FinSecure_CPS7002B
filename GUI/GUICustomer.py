# GUI/GUICustomer.py
import tkinter as tk
from tkinter import messagebox
import os
import csv
from utils import database, compliance

class CustomerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FinSecure - Customer Dashboard")
        self.logger = compliance.Compliance()
        self.customer = None
        self.show_login()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        tk.Label(self.master, text="Customer Login", font=("Arial", 16)).pack(pady=10)

        self.id_entry = self.create_input("Customer ID")
        self.name_entry = self.create_input("Name")

        def login():
            customer_id = self.id_entry.get()
            name = self.name_entry.get()
            customer = database.find_customer_by_id(customer_id)
            if customer and customer['name'] == name:
                self.customer = customer
                self.logger.log_event("CUSTOMER_LOGIN", f"{name} logged in.")
                self.dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid ID or Name.")
                self.logger.log_event("CUSTOMER_LOGIN_FAIL", f"Attempt with ID {customer_id} and name {name}")

        tk.Button(self.master, text="Login", command=login).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome {self.customer['name']}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.master, text="View My Profile", command=self.view_profile).pack(pady=5)
        tk.Button(self.master, text="View My Transactions", command=self.view_my_transactions).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.show_login).pack(pady=10)

    def create_scrollable_frame(self):
        container = tk.Frame(self.master)
        canvas = tk.Canvas(container, height=400)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def view_profile(self):
        self.clear_window()
        tk.Label(self.master, text="My Profile", font=("Arial", 14)).pack(pady=10)

        info = f"ID: {self.customer['customer_id']}\nName: {self.customer['name']}\nEmail: {self.customer['email']}\nBalance: ${self.customer['balance']}"
        tk.Label(self.master, text=info, justify="left").pack(pady=10)

        self.logger.log_event("VIEW_PROFILE", f"{self.customer['name']} viewed profile.")
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def view_my_transactions(self):
        self.clear_window()
        tk.Label(self.master, text="My Transactions", font=("Arial", 14)).pack(pady=10)

        frame = self.create_scrollable_frame()

        transactions_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "transactions.csv")

        found = False
        try:
            if not os.path.exists(transactions_file):
                raise FileNotFoundError

            with open(transactions_file, "r") as file:
                for line in file:
                    if line.startswith(self.customer['customer_id']):
                        found = True
                        tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)

            if not found:
                tk.Label(frame, text="No transactions found.", fg="gray").pack(pady=10)

            self.logger.log_event("VIEW_MY_TRANSACTIONS", f"{self.customer['name']} viewed their transactions.")
        except FileNotFoundError:
            messagebox.showerror("Error", "transactions.csv not found.")

        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def create_input(self, label):
        tk.Label(self.master, text=label).pack()
        entry = tk.Entry(self.master)
        entry.pack()
        return entry

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerGUI(root)
    root.mainloop()
