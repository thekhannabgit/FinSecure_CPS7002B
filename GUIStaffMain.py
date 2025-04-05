import tkinter as tk
from tkinter import messagebox
from staffdash import StaffDashboard


def staff_login():
    global dashboard  # Make it accessible to other functions
    username = username_entry.get()
    password = password_entry.get()

    dashboard = StaffDashboard()
    if dashboard.authenticate(username, password):
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Step 2: Staff Dashboard Window
def open_dashboard():
    dashboard_window = tk.Tk()
    dashboard_window.title("Staff Dashboard")
    dashboard_window.geometry("400x300")

    tk.Label(dashboard_window, text="Welcome to FinSecure Staff Dashboard", font=("Arial", 12)).pack(pady=10)

    tk.Button(dashboard_window, text="View Customers", command=lambda: dashboard.show_customers()).pack(pady=5)
    tk.Button(dashboard_window, text="Search Customer", command=lambda: dashboard.search_customer()).pack(pady=5)
    tk.Button(dashboard_window, text="View Transaction Report", command=lambda: dashboard.view_transactions()).pack(pady=5)
    tk.Button(dashboard_window, text="View Logs", command=lambda: dashboard.view_logs()).pack(pady=5)
    tk.Button(dashboard_window, text="Exit", command=dashboard_window.quit).pack(pady=10)

    dashboard_window.mainloop()

# Initialize Login Window
login_window = tk.Tk()
login_window.title("Staff Login")
login_window.geometry("300x200")

tk.Label(login_window, text="Username:").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password:").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=staff_login).pack(pady=10)

login_window.mainloop()
