# GUI/GUIStaff.py
import csv
import tkinter as tk
import os
from tkinter import messagebox, ttk
from utils import compliance, database

class StaffGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("FinSecure - Staff Dashboard")
        self.logger = compliance.Compliance()
        self.show_login()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Login", font=("Arial", 16)).pack(pady=10)

        self.user_entry = self.create_input("Username")
        self.pass_entry = self.create_input("Password", show="*")

        def attempt_login():
            if self.user_entry.get() == "admin" and self.pass_entry.get() == "admin123":
                self.logger.log_event("LOGIN", "Admin logged in.")
                self.dashboard()
            else:
                messagebox.showerror("Error", "Invalid credentials.")
                self.logger.log_event("FAILED_LOGIN", f"Attempt with username: {self.user_entry.get()}")

        tk.Button(self.master, text="Login", command=attempt_login).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.master, text="View All Customers", command=self.view_all_customers).pack(pady=5)
        tk.Button(self.master, text="Search Customer", command=self.search_customer).pack(pady=5)
        tk.Button(self.master, text="View Transactions", command=self.view_transactions).pack(pady=5)
        tk.Button(self.master, text="View Compliance Logs", command=self.view_logs).pack(pady=5)
        tk.Button(self.master, text="Logout", command=self.show_login).pack(pady=10)

    def view_all_customers(self):
        self.clear_window()
        tk.Label(self.master, text="All Customers", font=("Arial", 14)).pack(pady=10)

        for customer in database.get_all_customers():
            info = f"ID: {customer['customer_id']}, Name: {customer['name']}, Email: {customer['email']}, Balance: ${customer['balance']}"
            tk.Label(self.master, text=info, anchor="w", justify="left").pack(fill="x", padx=10)

        self.logger.log_event("VIEW_CUSTOMERS", "Viewed all customers.")
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def search_customer(self):
        self.clear_window()
        tk.Label(self.master, text="Search Customer by ID", font=("Arial", 14)).pack(pady=10)
        id_entry = tk.Entry(self.master)
        id_entry.pack(pady=5)

        def do_search():
            cust_id = id_entry.get()
            customer = database.find_customer_by_id(cust_id)
            if customer:
                info = f"ID: {customer['customer_id']}\nName: {customer['name']}\nEmail: {customer['email']}\nBalance: ${customer['balance']}"
                messagebox.showinfo("Customer Found", info)
                self.logger.log_event("SEARCH", f"Searched customer {cust_id}")
            else:
                messagebox.showerror("Not Found", f"Customer ID {cust_id} not found.")
                self.logger.log_event("SEARCH_FAIL", f"Customer {cust_id} not found")

        tk.Button(self.master, text="Search", command=do_search).pack(pady=5)
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

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

    def view_transactions(self):
        self.clear_window()
        tk.Label(self.master, text="Transactions Log", font=("Arial", 14)).pack(pady=10)

        frame = self.create_scrollable_frame()

        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        transactions_file = os.path.join(data_dir, "transactions.csv")

        try:
            if not os.path.exists(transactions_file):
                raise FileNotFoundError

            with open(transactions_file, "r") as file:
                lines = file.readlines()

            if len(lines) <= 1:
                messagebox.showinfo("No Transactions", "No transactions available yet.")
            else:
                for line in lines:
                    tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)

            self.logger.log_event("VIEW_TRANSACTIONS", "Viewed transaction log.")
        except FileNotFoundError:
            messagebox.showerror("Error", "transactions.csv not found.")

        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def view_logs(self):
        self.clear_window()
        tk.Label(self.master, text="Compliance Log", font=("Arial", 14)).pack(pady=10)

        frame = self.create_scrollable_frame()

        try:
            with open("data/audit_log.txt", "r") as file:
                for line in file:
                    tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)
            self.logger.log_event("VIEW_LOGS", "Viewed audit logs.")
        except:
            messagebox.showerror("Error", "audit_log.txt not found.")

        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def create_input(self, label, show=None):
        tk.Label(self.master, text=label).pack()
        entry = tk.Entry(self.master, show=show)
        entry.pack()
        return entry

if __name__ == "__main__":
    root = tk.Tk()
    app = StaffGUI(root)
    root.mainloop()
