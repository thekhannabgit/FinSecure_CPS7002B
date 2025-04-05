from Customer_Mngmnt import Customer
from staffdash import StaffDashboard

"""def customer_menu():
    print("\nWelcome, Customer!")
    # You can hardcode or take user input to select a customer
    customer = Customer(1, "John Doe", "john@example.com", 5000)
    customer.deposit(1000)
    customer.withdraw(200)"""

def customer_menu():
    print("\nWelcome, Customer!")
    customer = Customer(1, "John Doe", "john@example.com", 5000)

    while True:
        print("\n--- Customer Menu ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            customer.deposit(amount)
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            customer.withdraw(amount)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


def staff_menu():
    dashboard = StaffDashboard()
    if dashboard.login():
        dashboard.show_menu()
    else:
        print("Access Denied.")

if __name__ == "__main__":
    print("=== Welcome to FinSecure ===")
    print("1. Customer")
    print("2. Staff")
    role = input("Choose role: ")

    if role == "1":
        customer_menu()
    elif role == "2":
        staff_menu()
    else:
        print("Invalid choice.")
