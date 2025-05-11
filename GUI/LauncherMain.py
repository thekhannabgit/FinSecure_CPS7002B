import tkinter as tk
from tkinter import messagebox
from GUICustomer import CustomerGUI
from GUIStaff import StaffGUI
from utils import database

class Launcher:
    def __init__(self, master):
        self.master = master
        self.master.title("FinSecure - Unified Launcher")
        self.show_main_menu()

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.master, text="Welcome to FinSecure", font=("Arial", 18, "bold")).pack(pady=15)

        tk.Button(self.master, text="Customer Portal", width=25, command=self.launch_customer).pack(pady=10)
        tk.Button(self.master, text="Staff Login", width=25, command=self.staff_login_screen).pack(pady=10)
        tk.Button(self.master, text="Register Staff", width=25, command=self.register_staff_screen).pack(pady=10)
        tk.Button(self.master, text="Exit", width=25, command=self.master.quit).pack(pady=20)

    def launch_customer(self):
        self.clear_window()
        CustomerGUI(self.master)

    def staff_login_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Staff Login", font=("Arial", 14)).pack(pady=10)

        self.user_entry = self.create_input("Username")
        self.pass_entry = self.create_input("Password", show="*")

        def login():
            username = self.user_entry.get()
            password = self.pass_entry.get()
            role = database.validate_staff_login(username, password)
            if role:
                self.clear_window()
                StaffGUI(self.master, staff_username=username, staff_role=role)
            else:
                messagebox.showerror("Error", "Invalid staff credentials")

        tk.Button(self.master, text="Login", command=login).pack(pady=10)
        tk.Button(self.master, text="Back", command=self.show_main_menu).pack(pady=5)

    def register_staff_screen(self):
        self.clear_window()
        tk.Label(self.master, text="Register Staff", font=("Arial", 14)).pack(pady=10)

        self.new_user_entry = self.create_input("Username")
        self.new_pass_entry = self.create_input("Password", show="*")

        role_var = tk.StringVar(value="admin")
        tk.Label(self.master, text="Select Role:").pack()
        tk.Radiobutton(self.master, text="Admin", variable=role_var, value="admin").pack()
        tk.Radiobutton(self.master, text="Non-Admin", variable=role_var, value="non-admin").pack()

        def register():
            try:
                database.register_staff(
                    self.new_user_entry.get(),
                    self.new_pass_entry.get(),
                    role_var.get()
                )
                messagebox.showinfo("Success", "Staff registered successfully.")
                self.show_main_menu()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.master, text="Register", command=register).pack(pady=10)
        tk.Button(self.master, text="Back", command=self.show_main_menu).pack()

    def create_input(self, label, show=None):
        tk.Label(self.master, text=label).pack()
        entry = tk.Entry(self.master, show=show)
        entry.pack()
        return entry

if __name__ == "__main__":
    root = tk.Tk()
    Launcher(root)
    root.mainloop()
