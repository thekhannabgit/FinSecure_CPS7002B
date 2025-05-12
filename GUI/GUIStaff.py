import csv
import tkinter as tk
import os
from tkinter import messagebox
from utils import compliance, database, analytics, charting
from utils.database import TRANSACTIONS_FILE


class StaffGUI:
    def __init__(self, master, back_to_main=None):
        self.master = master
        self.master.geometry("700x550")
        self.master.title("FinSecure - Staff Dashboard")
        self.back_to_main = back_to_main
        self.logger = compliance.Compliance()
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)
        self.staff_username = None
        self.staff_role = None
        self.show_main_menu()
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        self.status_label = tk.Label(self.master, text="", fg="green", font=("Segoe UI", 10))
        self.status_label.pack(pady=5)

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Portal", font=("Segoe UI", 16, "bold")).pack(pady=20)

        tk.Button(self.master, text="Login", width=25, bg="#4caf50", fg="white", command=self.show_login).pack(pady=10)
        tk.Button(self.master, text="Register New Staff", width=25, bg="#007acc", fg="white", command=self.show_register).pack(pady=10)

        if self.back_to_main:
            tk.Button(self.master, text="⬅ Back to Main", width=25, bg="gray", fg="white", command=self.back_to_main).pack(pady=10)

        tk.Button(self.master, text="Exit", width=25, command=self.master.quit).pack(pady=30)

    def show_register(self):
        self.clear_window()
        tk.Label(self.master, text="Register New Staff", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.fullname_entry = self.create_input("Full Name")
        self.email_entry = self.create_input("Email")
        self.username_entry = self.create_input("Username")
        self.password_entry = self.create_input("Password", show="*")

        self.role_var = tk.StringVar(value="admin")
        tk.Label(self.master, text="Select Role:", font=("Segoe UI", 10)).pack()
        tk.Radiobutton(self.master, text="Admin", variable=self.role_var, value="admin").pack()
        tk.Radiobutton(self.master, text="Non-Admin", variable=self.role_var, value="non-admin").pack()

        def submit_registration():
            name = self.fullname_entry.get().strip()
            email = self.email_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            role = self.role_var.get()

            if not name or not email or not username or not password:
                self.status_label.config(text="❌ All fields are required.", fg="red")
                return

            try:
                database.save_staff({
                    "name": name,
                    "email": email,
                    "username": username,
                    "password": password,
                    "role": role
                })
                self.status_label.config(text="✅ Staff registered successfully!", fg="green")
            except ValueError as e:
                self.status_label.config(text=f"❌ {str(e)}", fg="red")

        tk.Button(self.master, text="Submit", command=submit_registration, bg="#2196f3", fg="white").pack(pady=10)
        tk.Button(self.master, text="⬅ Back", command=self.show_main_menu, bg="gray", fg="white").pack()

    def show_login(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Login", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.user_entry = self.create_input("Username")
        self.pass_entry = self.create_input("Password", show="*")

        def attempt_login():
            username = self.user_entry.get().strip()
            password = self.pass_entry.get().strip()
            role = database.validate_staff_login(username, password)

            if role:
                self.staff_username = username
                self.staff_role = role
                self.logger.log_event("LOGIN", f"{username} logged in as {role}")
                self.dashboard()
            else:
                self.status_label.config(text="❌ Invalid credentials.", fg="red")
                self.logger.log_event("FAILED_LOGIN", f"Failed login for {username}")

        tk.Button(self.master, text="Login", command=attempt_login, bg="#4caf50", fg="white").pack(pady=10)
        tk.Button(self.master, text="⬅ Back", command=self.show_main_menu, bg="gray", fg="white").pack()

    def dashboard(self):
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.staff_username} ({self.staff_role})", font=("Segoe UI", 14, "bold")).pack(pady=10)

        tk.Button(self.master, text="View All Customers", command=self.view_all_customers).pack(pady=8)
        tk.Button(self.master, text="Search Customer", command=self.search_customer).pack(pady=8)

        if self.staff_role == "admin":
            tk.Button(self.master, text="View Transactions", command=self.view_transactions).pack(pady=8)
            tk.Button(self.master, text="View Compliance Logs", command=self.view_logs).pack(pady=8)
            tk.Button(self.master, text="View Analytics", command=self.view_analytics).pack(pady=8)
            tk.Button(self.master, text="📊 Deposits vs Withdrawals", command=charting.plot_deposit_vs_withdrawal).pack(pady=8)
            tk.Button(self.master, text="📈 Customer Totals", command=charting.plot_customer_transaction_totals).pack(pady=8)

        tk.Button(self.master, text="Logout", command=self.show_main_menu).pack(pady=12)

    def view_all_customers(self):
        self.clear_window()
        tk.Label(self.master, text="All Customers", font=("Segoe UI", 14, "bold")).pack(pady=10)

        for customer in database.get_all_customers():
            info = f"ID: {customer['customer_id']}, Name: {customer['name']}, Email: {customer['email']}, Balance: ${customer['balance']}"
            tk.Label(self.master, text=info, anchor="w", justify="left").pack(fill="x", padx=10)

        self.logger.log_event("VIEW_CUSTOMERS", "Viewed all customers.")
        tk.Button(self.master, text="⬅ Back", command=self.dashboard).pack(pady=10)

    def search_customer(self):
        self.clear_window()
        tk.Label(self.master, text="Search Customer by ID", font=("Segoe UI", 14, "bold")).pack(pady=10)
        id_entry = tk.Entry(self.master)
        id_entry.pack(pady=5)

        def do_search():
            cust_id = id_entry.get()
            customer = database.find_customer_by_id(cust_id)
            if customer:
                info = f"✅ Found:\nID: {customer['customer_id']}\nName: {customer['name']}\nEmail: {customer['email']}\nBalance: ${customer['balance']}"
                self.status_label.config(text=info, fg="blue")
                self.logger.log_event("SEARCH", f"Searched customer {cust_id}")
            else:
                self.status_label.config(text=f"❌ Customer ID {cust_id} not found.", fg="red")

        tk.Button(self.master, text="Search", command=do_search, bg="#007acc", fg="white").pack(pady=5)
        tk.Button(self.master, text="⬅ Back", command=self.dashboard, bg="gray", fg="white").pack(pady=10)

    def view_transactions(self):
        self.clear_window()
        tk.Label(self.master, text="Transactions Log", font=("Segoe UI", 14, "bold")).pack(pady=10)
        frame = self.create_scrollable_frame()

        #transactions_file = os.path.join("data", "transactions.csv")
        transactions_file = TRANSACTIONS_FILE
        if os.path.exists(transactions_file):
            with open(transactions_file, "r") as file:
                lines = file.readlines()
            for line in lines:
                tk.Label(frame, text=line.strip(), anchor="w", justify="left").pack(fill="x", padx=10)
        else:
            self.status_label.config(text="No transactions found.", fg="red")

        self.logger.log_event("VIEW_TRANSACTIONS", "Viewed transaction log.")
        tk.Button(self.master, text="⬅ Back", command=self.dashboard).pack(pady=10)

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

        tk.Button(self.master, text="⬅ Back", command=self.dashboard).pack(pady=10)

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

        tk.Button(self.master, text="⬅ Back", command=self.dashboard).pack(pady=10)

    def create_scrollable_frame(self):
        container = tk.Frame(self.master)
        canvas = tk.Canvas(container, height=350)
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
        tk.Label(self.master, text=label, font=("Segoe UI", 10)).pack()
        entry = tk.Entry(self.master, show=show)
        entry.pack()
        return entry

    def on_exit(self):
        self.master.quit()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StaffGUI(root)
    root.mainloop()
