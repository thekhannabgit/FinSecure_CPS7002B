import csv
from datetime import datetime
import os


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")

CUSTOMER_FIELDS = ["customer_id", "name", "email", "password", "balance"]
TRANSACTION_FIELDS = ["transaction_id", "customer_id", "name", "type", "amount", "balance", "timestamp", "status"]

# Counter for transaction ID (will auto-increment)
transaction_counter = 1
if os.path.exists(TRANSACTIONS_FILE):
    with open(TRANSACTIONS_FILE, "r") as f:
        reader = list(csv.reader(f))
        if len(reader) > 1:
            try:
                last_id = reader[-1][0]
                if last_id.isdigit():
                    transaction_counter = int(last_id) + 1
            except:
                pass


os.makedirs(DATA_DIR, exist_ok=True)
#print(f"Data directory: {DATA_DIR}")
#print(f"Resolved path to customers.csv: {CUSTOMERS_FILE}")

session_customers = []

def load_customers_from_csv():
    if os.path.exists(CUSTOMERS_FILE):
        print(f"Loading customers from: {CUSTOMERS_FILE}")
        with open(CUSTOMERS_FILE, "r", newline="") as file:
            return list(csv.DictReader(file))
    print("No existing customers.csv found. Starting fresh.")
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
    global transaction_counter

    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Flagging logic
    if (txn_type == "Withdraw" and amount > 5000) or (txn_type == "Deposit" and amount > 10000):
        status = "Flagged for Review"
    else:
        status = "Approved"

    file_exists = os.path.exists(TRANSACTIONS_FILE)
    with open(TRANSACTIONS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(TRANSACTION_FIELDS)
        writer.writerow([
            transaction_counter,
            customer_id,
            name,
            txn_type,
            amount,
            balance,
            timestamp,
            status
        ])

    transaction_counter += 1


def persist_customers_to_csv():
    print(f"Persisting customers to: {CUSTOMERS_FILE}")
    with open(CUSTOMERS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CUSTOMER_FIELDS)
        writer.writeheader()
        for cust in session_customers:
            row = {field: cust.get(field, "") for field in CUSTOMER_FIELDS}
            writer.writerow(row)

if not os.path.exists(CUSTOMERS_FILE):
    print("Creating new customers.csv with headers.")
    persist_customers_to_csv()
'''else:
    print("customers.csv already exists.")'''

# === Staff Management ===
STAFF_FILE = os.path.join(DATA_DIR, "staff.csv")
STAFF_FIELDS = ["username", "password", "role"]

def load_all_staff():
    if not os.path.exists(STAFF_FILE):
        return []
    with open(STAFF_FILE, "r", newline="") as file:
        return list(csv.DictReader(file))

def find_staff(username):
    return next((s for s in load_all_staff() if s["username"] == username), None)

def validate_staff_login(username, password):
    staff = find_staff(username)
    if staff and staff["password"] == password:
        return staff["role"]  # returns 'admin' or 'non-admin'
    return None

def register_staff(username, password, role):
    if find_staff(username):
        raise ValueError("Username already exists.")
    with open(STAFF_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=STAFF_FIELDS)
        if os.stat(STAFF_FILE).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "username": username,
            "password": password,
            "role": role
        })

