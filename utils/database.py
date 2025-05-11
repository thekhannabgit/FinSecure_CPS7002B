# utils/database.py
import csv
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
STAFF_FILE = os.path.join(DATA_DIR, "staff.csv")

CUSTOMER_FIELDS = ["customer_id", "name", "email", "password", "balance"]
TRANSACTION_FIELDS = ["customer_id", "name", "type", "amount", "balance"]
STAFF_FIELDS = ["name", "email", "username", "password", "role"]

os.makedirs(DATA_DIR, exist_ok=True)

session_customers = []

def load_customers_from_csv():
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "r", newline="") as file:
            return list(csv.DictReader(file))
    return []

session_customers.extend(load_customers_from_csv())

def get_all_customers():
    return session_customers

def find_customer_by_id(customer_id):
    return next((c for c in session_customers if c["customer_id"] == customer_id), None)

def find_customer_by_email(email):
    return next((c for c in session_customers if c["email"] == email), None)

def save_customer(customer_dict):
    if find_customer_by_email(customer_dict["email"]):
        raise ValueError("Email already registered.")
    if find_customer_by_id(customer_dict["customer_id"]):
        raise ValueError("Customer ID already exists.")
    session_customers.append(customer_dict)
    persist_customers_to_csv()

def update_customer_balance(customer_id, new_balance):
    for customer in session_customers:
        if customer["customer_id"] == customer_id:
            customer["balance"] = str(new_balance)
            break
    persist_customers_to_csv()

def log_transaction(customer_id, name, txn_type, amount, balance):
    file_exists = os.path.exists(TRANSACTIONS_FILE)
    with open(TRANSACTIONS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(TRANSACTION_FIELDS)
        writer.writerow([customer_id, name, txn_type, amount, balance])

def persist_customers_to_csv():
    with open(CUSTOMERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CUSTOMER_FIELDS)
        writer.writeheader()
        for cust in session_customers:
            writer.writerow(cust)

# ================= STAFF METHODS ===================

def save_staff(staff_dict):
    if not os.path.exists(STAFF_FILE):
        with open(STAFF_FILE, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=STAFF_FIELDS)
            writer.writeheader()

    existing_users = []
    if os.path.exists(STAFF_FILE):
        with open(STAFF_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)
            existing_users = list(reader)

    for user in existing_users:
        if user["username"] == staff_dict["username"]:
            raise ValueError("Username already exists.")

    with open(STAFF_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=STAFF_FIELDS)
        writer.writerow(staff_dict)

def validate_staff_login(username, password):
    if not os.path.exists(STAFF_FILE):
        return None
    with open(STAFF_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["username"] == username and row["password"] == password:
                return row["role"]  # Return 'admin' or 'non-admin'
    return None

if not os.path.exists(CUSTOMERS_FILE):
    persist_customers_to_csv()
