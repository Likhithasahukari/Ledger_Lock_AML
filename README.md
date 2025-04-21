# 🛡️ Ledger-Lock: Blockchain-Powered Anti-Money Laundering System

A lightweight and intuitive web application built using **Flask** that leverages **blockchain principles** to detect and log suspicious financial transactions in real time. The system supports **KYC verification**, **risk analysis**, **fraud detection**, and **immutable ledger tracking**.

---

## 🚀 Features

### 🔐 KYC Registration
- User form for inputting identity details.
- KYC status is set to `Verified` if the user is from India (IN), USA (US), or Singapore (SG).
- All user data is stored in `kyc_users.json`.

### 💸 Transaction Monitoring
- Transactions are checked against KYC-verified users.
- Risk-based analysis using:
  - Transaction amount
  - Speed of transaction
  - Randomized risk injection
- Transactions are flagged if risk score ≥ 50.
- All transactions are logged in `transactions.json`.

### ⛓️ Blockchain Ledger
- Every transaction is added to a blockchain-style ledger.
- Each block contains:
  - Transaction details
  - Previous hash
  - SHA-256 hash of the current block
- Ledger is stored in `ledger.json`.

### 🧾 KYC Status Checker
- Verify if a user is KYC approved using their ID.

---

## 🛠️ Tech Stack

- 💻 **Backend**: Flask (Python)
- 📂 **Data Storage**: JSON files (`kyc_users.json`, `transactions.json`, `ledger.json`)
- 🎨 **Frontend**: HTML Templates via Jinja2
