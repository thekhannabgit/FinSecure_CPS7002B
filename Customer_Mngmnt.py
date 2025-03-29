from database import Database
from Transactions import Transaction
from compliance import Compliance

class Customer:
    def __init__(self, customer_id, name, email, balance=0):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.balance = balance
        self.db = Database()
        self.txn = Transaction()
        self.compliance = Compliance()

    def deposit(self, amount):
        self.balance += amount
        self.db.update_balance(self.customer_id, self.balance)
        status = self.txn.record_transaction(self.customer_id * 100 + 1, self.customer_id, "Deposit", amount)
        self.compliance.log_event("DEPOSIT", f"{self.name} deposited ${amount}. Status: {status}")
        print(f"{self.name} deposited {amount}. New balance: {self.balance}. Status: {status}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Insufficient funds for {self.name}")
            self.compliance.log_event("FAILED_WITHDRAWAL", f"{self.name} attempted to withdraw ${amount} (Insufficient Funds).")
        else:
            self.balance -= amount
            self.db.update_balance(self.customer_id, self.balance)
            status = self.txn.record_transaction(self.customer_id * 100 + 2, self.customer_id, "Withdrawal", amount)
            self.compliance.log_event("WITHDRAWAL", f"{self.name} withdrew ${amount}. Status: {status}")
            print(f"{self.name} withdrew {amount}. New balance: {self.balance}. Status: {status}")

# Example Usage
if __name__ == "__main__":
    customer = Customer(1, "John Doe", "john@example.com", 5000)
    customer.deposit(3000)
    customer.withdraw(7000)  # This should be flagged for fraud
