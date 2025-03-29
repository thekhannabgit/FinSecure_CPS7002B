import csv
import os


class Database:
    def __init__(self, filename="customers.csv"):
        self.filename = filename
        # If the file doesn't exist, create it with headers
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Customer ID", "Name", "Email", "Balance"])

    def add_customer(self, customer_id, name, email, balance=0):
        """Adds a new customer to the database."""
        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([customer_id, name, email, balance])

    def get_customers(self):
        """Retrieves all customers from the database."""
        customers = []
        with open(self.filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                customers.append(row)
        return customers

    def update_balance(self, customer_id, new_balance):
        """Updates the balance of a specific customer."""
        rows = []
        with open(self.filename, mode="r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        for row in rows:
            if row[0] == str(customer_id):
                row[3] = new_balance  # Update balance column

        with open(self.filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)


# Testing the database
if __name__ == "__main__":
    db = Database()
    db.add_customer(1, "John Doe", "john@example.com", 500)
    db.add_customer(2, "Alice Smith", "alice@example.com", 1000)

    print("Customer List:")
    customers = db.get_customers()
    for customer in customers:
        print(customer)
