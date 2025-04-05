from datetime import datetime


class Compliance:
    def __init__(self, log_file="audit_log.txt"):
        self.log_file = log_file

    def log_event(self, event_type, details):
        """Logs an event with timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {event_type}: {details}\n"

        with open(self.log_file, mode="a") as file:
            file.write(log_entry)

    def review_logs(self):
        """Displays audit logs."""
        try:
            with open(self.log_file, mode="r") as file:
                logs = file.readlines()
                return logs
        except FileNotFoundError:
            return ["No logs found."]


# Testing Compliance Logging
if __name__ == "__main__":
    compliance = Compliance()
    compliance.log_event("LOGIN_ATTEMPT", "User John Doe tried to log in.")
    compliance.log_event("SUSPICIOUS_TRANSACTION", "Customer 1 withdrew $7000 (Flagged).")

    print("Audit Log Review:")
    print("".join(compliance.review_logs()))
