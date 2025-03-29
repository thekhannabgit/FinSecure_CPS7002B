import hashlib
import csv
import os

class Security:
    def __init__(self, users_file="users.csv"):
        self.users_file = users_file

        if not os.path.exists(self.users_file):
            with open(self.users_file, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Username", "Password Hash"])

    def hash_password(self, password):
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, username, password):
        """Registers a new user with a hashed password."""
        hashed_password = self.hash_password(password)

        with open(self.users_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, hashed_password])

        print(f"User {username} registered successfully.")

    def login_user(self, username, password):
        """Validates user login."""
        hashed_password = self.hash_password(password)

        with open(self.users_file, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Username"] == username and row["Password Hash"] == hashed_password:
                    print("Login successful!")
                    return True

        print("Invalid username or password.")
        return False

# Testing the Security System
if __name__ == "__main__":
    sec = Security()
    sec.register_user("admin", "securepassword123")  # Register a user
    sec.login_user("admin", "securepassword123")  # Successful login
    sec.login_user("admin", "wrongpassword")  # Failed login
