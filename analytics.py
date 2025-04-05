import csv
import matplotlib.pyplot as plt
from compliance import Compliance


class Analytics:
    def __init__(self, transactions_file="transactions.csv"):
        self.transactions_file = transactions_file
        self.compliance = Compliance()

    def calculate_totals(self):
        """Calculates total deposits, withdrawals, and flagged transactions."""
        total_deposits = 0
        total_withdrawals = 0
        flagged_transactions = 0

        with open(self.transactions_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                amount = float(row["Amount"])
                if row["Type"] == "Deposit":
                    total_deposits += amount
                elif row["Type"] == "Withdrawal":
                    total_withdrawals += amount

                if row["Status"] == "Flagged for Review":
                    flagged_transactions += 1

        return total_deposits, total_withdrawals, flagged_transactions

    def generate_report(self):
        """Displays transaction statistics and logs report generation."""
        total_deposits, total_withdrawals, flagged = self.calculate_totals()

        report = f"\n===== Financial Report =====\n" \
                 f"Total Deposits: ${total_deposits}\n" \
                 f"Total Withdrawals: ${total_withdrawals}\n" \
                 f"Flagged Transactions: {flagged}\n" \
                 f"============================\n"

        print(report)
        self.compliance.log_event("REPORT_GENERATED", "Financial report generated.")

    def visualize_transactions(self):
        """Generates a bar chart for deposits vs withdrawals."""
        total_deposits, total_withdrawals, _ = self.calculate_totals()

        categories = ["Deposits", "Withdrawals"]
        values = [total_deposits, total_withdrawals]

        plt.bar(categories, values, color=["green", "red"])
        plt.xlabel("Transaction Type")
        plt.ylabel("Amount ($)")
        plt.title("Total Deposits vs Withdrawals")
        plt.show()


# Testing Analytics
if __name__ == "__main__":
    analytics = Analytics()
    analytics.generate_report()
    analytics.visualize_transactions()
