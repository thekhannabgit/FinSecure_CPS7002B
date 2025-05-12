import tkinter as tk
from GUICustomer import CustomerGUI
from GUIStaff import StaffGUI

def open_customer_gui():
    root.withdraw()
    new_root = tk.Toplevel()
    CustomerGUI(new_root, back_to_main=lambda: return_to_main(new_root))

def open_staff_gui():
    root.withdraw()
    new_root = tk.Toplevel()
    StaffGUI(new_root, back_to_main=lambda: return_to_main(new_root))

def return_to_main(window):
    window.destroy()
    root.deiconify()

def quit_app():
    root.destroy()

root = tk.Tk()
root.title("FinSecure Launcher")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Welcome to FinSecure", font=("Segoe UI", 18, "bold"), bg="#f0f0f0").pack(pady=30)

tk.Button(root, text="Customer Portal", width=25, bg="#007acc", fg="white",
          font=("Segoe UI", 12), command=open_customer_gui).pack(pady=10)

tk.Button(root, text="Staff Portal", width=25, bg="#4caf50", fg="white",
          font=("Segoe UI", 12), command=open_staff_gui).pack(pady=10)

tk.Button(root, text="Exit", width=25, bg="gray", fg="white",
          font=("Segoe UI", 12), command=quit_app).pack(pady=30)

root.mainloop()
