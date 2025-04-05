from Customer_Mngmnt import Customer
from database import Database
from analytics import Analytics
from compliance import Compliance
from security import Security
import tkinter as tk
from tkinter import messagebox

class StaffDashboard:
    def __init__(self):
        self.db = Database()
        self.analytics = Analytics()
        self.compliance = Compliance()
        self.security = Security()
        self.customers = [
            Customer("C001", "John Doe", 5000),
            Customer("C002", "Jane Smith", 3000)
        ]

    def login(self):
        """Login before accessing dashboard."""
        username = input("Username: ")
        password = input("Password: ")
        return self.security.login_user(username, password)

    def show_customers(self):
        if not self.customers:
            messagebox.showinfo("Customers", "No customers found.")
            return

        # Create a new popup window
        customer_window = tk.Toplevel()
        customer_window.title("Customer List")
        customer_window.geometry("400x300")

        tk.Label(customer_window, text="Customer Records", font=("Arial", 14)).pack(pady=10)

        # Show each customer in a label
        for customer in self.customers:
            info = f"ID: {customer.customer_id} | Name: {customer.name} | Balance: {customer.balance}"
            tk.Label(customer_window, text=info, anchor="w", justify="left").pack(padx=10, anchor="w")

    def view_all_customers(self):
        print("\n--- All Customers ---")
        with open("customers.csv", mode="r") as file:
            for line in file:
                print(line.strip())

    def search_customer(self):
        cust_id = input("Enter Customer ID to search: ")
        found = False
        with open("customers.csv", mode="r") as file:
            for line in file:
                if line.startswith(cust_id + ","):
                    print("Customer Found: ", line.strip())
                    found = True
                    break
        if not found:
            print("Customer not found.")

    def view_logs(self):
        print("\n--- Compliance Logs ---")
        #with open("audit_logs.txt", "r") as log_file:

        with open("audit_log.txt", "r") as log_file:
            for line in log_file:
                print(line.strip())

    '''def authenticate(self, username, password):
        pass'''

    def authenticate(self, username, password):
        # Replace with your real auth logic
        return username == "admin" and password == "securepassword123"

    def search_customer(self):
        def perform_search():
            cid = entry_id.get()
            for customer in self.customers:
                if customer.customer_id == cid:
                    result = f"ID: {customer.customer_id}\nName: {customer.name}\nBalance: {customer.balance}"
                    messagebox.showinfo("Customer Found", result)
                    return
            messagebox.showerror("Not Found", f"No customer found with ID {cid}")

        search_window = tk.Toplevel()
        search_window.title("Search Customer")
        search_window.geometry("300x150")

        tk.Label(search_window, text="Enter Customer ID:").pack(pady=5)
        entry_id = tk.Entry(search_window)
        entry_id.pack(pady=5)

        tk.Button(search_window, text="Search", command=perform_search).pack(pady=10)

    def view_transactions(self):
        try:
            with open("transactions.csv", "r") as report_file:
            #with open("report.txt", "r") as report_file:
                report_data = report_file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction report not found.")
            return

        report_window = tk.Toplevel()
        report_window.title("Transaction Report")
        report_window.geometry("500x400")

        tk.Label(report_window, text="Transaction Report", font=("Arial", 14)).pack(pady=10)

        text_area = tk.Text(report_window, wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        text_area.insert("1.0", report_data)
        text_area.config(state="disabled")  # Read-only

    def view_compliance_logs(self):
        try:
            with open("audit_log.txt", "r") as log_file:
                logs = log_file.read()
        except FileNotFoundError:
            messagebox.showerror("Error", "Compliance log file not found.")
            return

        log_window = tk.Toplevel()
        log_window.title("Compliance Logs")
        log_window.geometry("500x400")

        tk.Label(log_window, text="Compliance Logs", font=("Arial", 14)).pack(pady=10)

        text_area = tk.Text(log_window, wrap="word")
        text_area.pack(expand=True, fill="both", padx=10, pady=10)
        text_area.insert("1.0", logs)
        text_area.config(state="disabled")


# Running the dashboard
if __name__ == "__main__":
    dashboard = StaffDashboard()
    if dashboard.login():
        dashboard.show_menu()
    else:
        print("Access Denied.")
