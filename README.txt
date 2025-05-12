# 💼 FinSecure - Financial Services Management System

FinSecure is a secure, GUI-based financial service system built using Python. It offers a centralized dashboard for **customers** and **staff** to manage core banking operations, including:

- Customer registration and login
- Deposits and withdrawals with compliance logging
- Staff (admin/non-admin) portal with analytics, transaction logs, and audit log access
- Data visualization through pie and bar charts using `matplotlib`

---

## 📁 Project Structure

```
FinSecure/
├─ LauncherMain.py               # Entry point to select Customer or Staff dashboard
├─ gui/
│   ├─ customer_gui.py           # GUI for customer portal
│   └─ staff_gui.py              # GUI for staff dashboard
├─ utils/
│   ├─ database.py               # Manages CSV data persistence
│   ├─ compliance.py            # Logs compliance and actions
│   ├─ analytics.py             # Summary analytics calculations
│   └─ charting.py              # Pie/Bar chart visualizations using matplotlib
├─ data/
│   ├─ customers.csv             # Customer records
│   ├─ staff.csv                 # Staff records (admin/non-admin)
│   ├─ transactions.csv          # All transactions with status
│   └─ audit_log.txt             # Compliance and access logs
```

---

## ✅ Requirements

Make sure you have Python 3.10+ and the required dependencies installed.

### 📦 Install required packages

```bash
pip install matplotlib
```

----

## 🚀 How to Run

1. **Clone or download the project** into a folder:
2. **Run the main launcher GUI**:
3. **Please maximise the window to use back button for navigation

```bash
python LauncherMain.py
```

3. **Select**:
   - **Customer Portal** → Register or login as a customer
   - **Staff Portal** → Register/login as staff (admin/non-admin)

---

## 👤 Customer Features

| Feature           | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| Register          | Create a new customer with name, email, and password                        |
| Login             | Secure login using Customer ID and password                                 |
| Deposit/Withdraw  | Perform transactions with real-time balance updates                         |
| Balance Check     | View current balance without popups                                         |
| GUI Only          | No command line interface; intuitive GUI interface throughout               |

---

## 🧑‍💼 Staff Features

| Feature                  | Admin     | Non-Admin | Description                                       |
|--------------------------|-----------|-----------|---------------------------------------------------|
| Register staff           | ✔️         | ✔️         | Register new staff with name, email, username     |
| Login                    | ✔️         | ✔️         | Secure login via username/password                |
| View all customers       | ✔️         | ✔️         | View list of all registered customers             |
| Search customers         | ✔️         | ✔️         | Search by Customer ID                             |
| View transaction log     | ✔️         | ❌         | Admin-only: shows all transaction records         |
| View compliance log      | ✔️         | ❌         | Admin-only: access audit events                   |
| View analytics           | ✔️         | ❌         | Admin-only: total deposits, top customer etc.     |
| Charts                   | ✔️         | ❌         | Bar & Pie charts for data visualization           |

---

## 📊 Sample Charts

- **Pie Chart**: Breakdown of Deposits vs Withdrawals
- **Bar Chart**: Customers vs Total Transaction Amounts

Charts are generated using `matplotlib` and display in popup windows on admin access.

---

## 🔐 Compliance & Logging

- All significant events (logins, transactions, searches) are logged to `audit_log.txt`.
- Transactions exceeding thresholds are flagged for review.

---

## 🧪 Test Users

You can register your own users via the GUI. But here’s a quick reference if needed:

- **Customer**:
  - Register with any name/email/password.
- **Staff (Admin)**:
  - Register with desired username/password.
  - Choose **admin** role during registration.

  - **Customer Test User**:
  - Username: CUST4103
  - password: 2416877
- **Staff Test user (Admin)**:
  - Username: admin
  - password: 2416877

---

## 💾 Data Persistence

All data is stored locally in `.csv` files inside the `data/` folder.

| File              | Purpose                                |
|-------------------|----------------------------------------|
| `customers.csv`   | All customer data                      |
| `staff.csv`       | Staff credentials and role             |
| `transactions.csv`| Transactions history with status       |
| `audit_log.txt`   | Action logs (logins, search, etc)      |

---

## 📌 Notes

- Project is designed for GUI-only usage.
- Make sure to close the GUI windows completely before restarting to avoid conflict.
- Exiting from **LauncherMain.py** will close the entire application.

---

## 📞 Support

This project was developed for academic purposes in support of CPS7002B assessment. For any queries or issues, contact the developer via project repository or university channels.

---

**Happy Banking! 💸**