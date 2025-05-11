import csv
import tkinter as tk
import os
from tkinter import messagebox
from utils import compliance, database, analytics, charting

class StaffGUI:
    def __init__(self, master, staff_username="Unknown", staff_role="non-admin"):
        self.master = master
        self.staff_username = staff_username
        self.staff_role = staff_role
        self.master.title(f"FinSecure - Staff Dashboard ({self.staff_role.title()})")
        self.logger = compliance.Compliance()
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)
        self.show_login()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)

    def show_login(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Login", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.user_entry = self.create_input("Username")
        self.pass_entry = self.create_input("Password", show="*")

        def attempt_login():
            if self.user_entry.get() == "admin" and self.pass_entry.get() == "admin123":
                self.logger.log_event("LOGIN", "Admin logged in.")
                self.dashboard()
            else:
                role = database.validate_staff_login(self.user_entry.get(), self.pass_entry.get())
                if role:
                    self.staff_username = self.user_entry.get()
                    self.staff_role = role
                    self.logger.log_event("LOGIN", f"{self.staff_username} logged in as {self.staff_role}")
                    self.dashboard()
                else:
                    self.status_label.config(text="❌ Invalid credentials.", fg="red")
                    self.logger.log_event("FAILED_LOGIN", f"Attempt with username: {self.user_entry.get()}")

        tk.Button(self.master, text="Login", command=attempt_login).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.staff_username}", font=("Segoe UI", 14, "bold")).pack(pady=10)

        tk.Button(self.master, text="View All Customers", command=self.view_all_customers).pack(pady=8)
        tk.Button(self.master, text="Search Customer", command=self.search_customer).pack(pady=8)

        if self.staff_role == "admin":
            tk.Button(self.master, text="View Transactions", command=self.view_transactions).pack(pady=8)
            tk.Button(self.master, text="View Compliance Logs", command=self.view_logs).pack(pady=8)
            tk.Button(self.master, text="View Analytics", command=self.view_analytics).pack(pady=8)
            tk.Button(self.master, text="📊 Deposits vs Withdrawals", command=charting.plot_deposit_vs_withdrawal).pack(pady=8)
            tk.Button(self.master, text="📈 Customer Totals", command=charting.plot_customer_transaction_totals).pack(pady=8)

        tk.Button(self.master, text="Logout", command=self.show_login).pack(pady=12)

    def view_all_customers(self):
        self.clear_window()
        tk.Label(self.master, text="All Customers", font=("Segoe UI", 14, "bold")).pack(pady=10)

        for customer in database.get_all_customers():
            info = f"ID: {customer['customer_id']}, Name: {customer['name']}, Email: {customer['email']}, Balance: ${customer['balance']}"
            tk.Label(self.master, text=info, anchor="w", justify="left").pack(fill="x", padx=10)

        self.logger.log_event("VIEW_CUSTOMERS", "Viewed all customers.")
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def search_customer(self):
        self.clear_window()
        tk.Label(self.master, text="Search Customer by ID", font=("Segoe UI", 14, "bold")).pack(pady=10)
        id_entry = tk.Entry(self.master)
        id_entry.pack(pady=5)

        def do_search():
            cust_id = id_entry.get()
            customer = database.find_customer_by_id(cust_id)
            if customer:
                info = f"ID: {customer['customer_id']}\nName: {customer['name']}\nEmail: {customer['email']}\nBalance: ${customer['balance']}"
                self.status_label.config(text=info, fg="blue")
                self.logger.log_event("SEARCH", f"Searched customer {cust_id}")
            else:
                self.status_label.config(text=f"❌ Customer ID {cust_id} not found.", fg="red")
                self.logger.log_event("SEARCH_FAIL", f"Customer {cust_id} not found")

        tk.Button(self.master, text="Search", command=do_search).pack(pady=5)
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def view_transactions(self):
        self.clear_window()
        tk.Label(self.master, text="Transactions Log", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame = self.create_scrollable_frame()

        transactions_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "transactions.csv")

        try:
            if not os.path.exists(transactions_file):
                raise FileNotFoundError

            with open(transactions_file, "r") as file:
                lines = file.readlines()

            if len(lines) <= 1:
                self.status_label.config(text="No transactions available yet.", fg="blue")
            else:
                for line in lines:
                    tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)

            self.logger.log_event("VIEW_TRANSACTIONS", "Viewed transaction log.")
        except FileNotFoundError:
            self.status_label.config(text="transactions.csv not found.", fg="red")

        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def view_logs(self):
        self.clear_window()
        tk.Label(self.master, text="Compliance Log", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame = self.create_scrollable_frame()

        try:
            with open("data/audit_log.txt", "r") as file:
                for line in file:
                    tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)
            self.logger.log_event("VIEW_LOGS", "Viewed audit logs.")
        except:
            self.status_label.config(text="audit_log.txt not found.", fg="red")

        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def view_analytics(self):
        self.clear_window()
        tk.Label(self.master, text="Data Analytics Summary", font=("Segoe UI", 14, "bold")).pack(pady=10)

        frame = self.create_scrollable_frame()
        summary = analytics.get_analytics_summary()

        lines = [
            f"📊 Total Customers: {summary['total_customers']}",
            f"💰 Total Deposits: ${summary['total_deposits']:.2f}",
            f"💸 Total Withdrawals: ${summary['total_withdrawals']:.2f}",
            f"📈 Highest Deposit: ${summary['highest_deposit']:.2f}",
            f"📉 Highest Withdrawal: ${summary['highest_withdrawal']:.2f}",
            f"💼 Average Balance: ${summary['average_balance']:.2f}",
        ]

        if summary['top_customer']:
            top = summary['top_customer']
            lines.append(f"🏆 Top Customer: {top['name']} (ID: {top['customer_id']}) with ${top['balance']}")

        for line in lines:
            tk.Label(frame, text=line, anchor="w", justify="left").pack(fill="x", padx=10)

        self.logger.log_event("VIEW_ANALYTICS", "Viewed analytics summary.")
        tk.Button(self.master, text="Back", command=self.dashboard).pack(pady=10)

    def create_scrollable_frame(self):
        container = tk.Frame(self.master)
        canvas = tk.Canvas(container, height=400)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        container.pack(fill="both", expand=True)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def create_input(self, label, show=None):
        tk.Label(self.master, text=label).pack()
        entry = tk.Entry(self.master, show=show)
        entry.pack()
        return entry

if __name__ == "__main__":
    root = tk.Tk()
    app = StaffGUI(root)
    root.mainloop()
