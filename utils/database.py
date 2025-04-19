import csv
import os

# Get absolute path to the project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Use absolute paths for data files
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")

# Field definitions
CUSTOMER_FIELDS = ["customer_id", "name", "email", "password", "balance"]
TRANSACTION_FIELDS = ["customer_id", "name", "type", "amount", "balance"]

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)
#print(f"Data directory: {DATA_DIR}")
#print(f"Resolved path to customers.csv: {CUSTOMERS_FILE}")

# Session data
session_customers = []

# Load existing customers from CSV
def load_customers_from_csv():
    if os.path.exists(CUSTOMERS_FILE):
        print(f"Loading customers from: {CUSTOMERS_FILE}")
        with open(CUSTOMERS_FILE, "r", newline="") as file:
            return list(csv.DictReader(file))
    print("No existing customers.csv found. Starting fresh.")
    return []

# Load into session
session_customers.extend(load_customers_from_csv())

# Public API functions
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
    print(f"Persisting customers to: {CUSTOMERS_FILE}")
    with open(CUSTOMERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CUSTOMER_FIELDS)
        writer.writeheader()
        for cust in session_customers:
            row = {field: cust.get(field, "") for field in CUSTOMER_FIELDS}
            writer.writerow(row)

# Ensure an empty file is created with headers if file was deleted
if not os.path.exists(CUSTOMERS_FILE):
    print("Creating new customers.csv with headers.")
    persist_customers_to_csv()
'''else:
    print("customers.csv already exists.")'''
