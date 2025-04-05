import csv
import os
from datetime import datetime
from compliance import Compliance

class Transaction:
    def __init__(self, filename="transactions.csv"):
        self.filename = filename
        self.compliance = Compliance()

        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Transaction ID", "Customer ID", "Type", "Amount", "Date", "Status"])

    def record_transaction(self, transaction_id, customer_id, txn_type, amount):
        """Records a transaction and logs compliance issues."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Approved"

        if self.is_fraudulent(amount):
            status = "Flagged for Review"
            self.compliance.log_event("SUSPICIOUS_TRANSACTION",
                                      f"Customer {customer_id} tried {txn_type} of ${amount} (Flagged).")

        with open(self.filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([transaction_id, customer_id, txn_type, amount, date, status])

        return status

    def is_fraudulent(self, amount):
        """Flags transactions above a certain threshold as suspicious."""
        fraud_threshold = 5000
        return amount > fraud_threshold
