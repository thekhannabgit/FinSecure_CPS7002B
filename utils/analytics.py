import csv
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")

def get_analytics_summary():
    total_customers = 0
    total_deposits = 0
    total_withdrawals = 0
    highest_deposit = 0
    highest_withdrawal = 0
    balances = []
    top_customer = None

    # Read customers
    if os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, "r") as file:
            reader = csv.DictReader(file)
            customers = list(reader)
            total_customers = len(customers)
            for row in customers:
                try:
                    balances.append(float(row["balance"]))
                except:
                    pass

            if customers:
                top_customer = max(customers, key=lambda c: float(c["balance"]))

    # Read transactions
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    amount = float(row["amount"])
                    if row["type"].lower() == "deposit":
                        total_deposits += amount
                        highest_deposit = max(highest_deposit, amount)
                    elif row["type"].lower() == "withdraw":
                        total_withdrawals += amount
                        highest_withdrawal = max(highest_withdrawal, amount)
                except:
                    pass

    avg_balance = round(sum(balances) / len(balances), 2) if balances else 0

    return {
        "total_customers": total_customers,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "highest_deposit": highest_deposit,
        "highest_withdrawal": highest_withdrawal,
        "average_balance": avg_balance,
        "top_customer": top_customer
    }
