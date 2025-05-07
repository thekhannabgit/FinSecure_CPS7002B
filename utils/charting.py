import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")


def plot_deposit_vs_withdrawal():
    deposits = 0
    withdrawals = 0

    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    amount = float(row["amount"])
                    if row["type"].lower() == "deposit":
                        deposits += amount
                    elif row["type"].lower() == "withdraw":
                        withdrawals += amount
                except:
                    continue

    labels = ["Deposits", "Withdrawals"]
    values = [deposits, withdrawals]
    colors = ["#4CAF50", "#F44336"]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
    plt.title("Deposits vs Withdrawals")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()


def plot_customer_transaction_totals():
    customer_totals = defaultdict(float)

    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    name = row["name"]
                    amount = float(row["amount"])
                    customer_totals[name] += amount
                except:
                    continue

    if not customer_totals:
        print("No transaction data available.")
        return

    names = list(customer_totals.keys())
    totals = list(customer_totals.values())

    plt.figure(figsize=(10, 6))
    plt.bar(names, totals, color="#2196F3")
    plt.xlabel("Customer")
    plt.ylabel("Total Transaction Volume")
    plt.title("Total Transactions by Customer")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
