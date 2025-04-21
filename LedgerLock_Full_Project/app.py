from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import hashlib
import random
import time
import uuid

app = Flask(__name__)

# File paths
KYC_FILE = "kyc_users.json"
TRANSACTION_FILE = "transactions.json"
LEDGER_FILE = "ledger.json"

def read_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def write_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def sha256_hash(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

@app.route("/")
def index():
    kyc_users = read_json(KYC_FILE)
    transactions = read_json(TRANSACTION_FILE)
    ledger = read_json(LEDGER_FILE)
    verified_count = sum(1 for u in kyc_users if u["kyc_status"] == "Verified")
    flagged_count = sum(1 for t in transactions if t["status"] == "Flagged")
    return render_template("index.html", kyc_users=kyc_users, transactions=transactions,
                           ledger=ledger, verified_count=verified_count,
                           flagged_count=flagged_count)

@app.route("/kyc", methods=["GET", "POST"])
def kyc():
    if request.method == "POST":
        data = request.form.to_dict()
        data["kyc_status"] = "Verified" if data["country"] in ["IN", "US", "SG"] else "Not Verified"
        users = read_json(KYC_FILE)
        users.append(data)
        write_json(KYC_FILE, users)
        return redirect(url_for("kyc"))
    return render_template("kyc.html")

@app.route("/transaction", methods=["GET", "POST"])
def transaction():
    result = None
    if request.method == "POST":
        data = request.form.to_dict()
        users = read_json(KYC_FILE)
        user_ids = [u["user_id"] for u in users if u["kyc_status"] == "Verified"]
        if data["sender_id"] not in user_ids or data["receiver_id"] not in user_ids:
            result = {"error": "KYC not verified for sender or receiver."}
        else:
            risk = 0
            amount = float(data["amount"])
            speed = int(data["transaction_speed"])
            if amount > 25000: risk += 50
            if speed < 2: risk += 30
            risk += random.randint(0, 20)
            status = "Flagged" if risk >= 50 else "Approved"

            transaction_record = {
                "id": str(uuid.uuid4()),
                "timestamp": time.time(),
                "sender_id": data["sender_id"],
                "receiver_id": data["receiver_id"],
                "amount": amount,
                "sender_country": data["sender_country"],
                "receiver_country": data["receiver_country"],
                "speed": speed,
                "risk_score": risk,
                "status": status
            }

            transactions = read_json(TRANSACTION_FILE)
            transactions.append(transaction_record)
            write_json(TRANSACTION_FILE, transactions)

            # Blockchain logic
            ledger = read_json(LEDGER_FILE)
            previous_hash = ledger[-1]["hash"] if ledger else "0"
            block = {
                "index": len(ledger) + 1,
                "timestamp": time.time(),
                "transaction": transaction_record,
                "previous_hash": previous_hash
            }
            block["hash"] = sha256_hash(block)
            ledger.append(block)
            write_json(LEDGER_FILE, ledger)

            result = transaction_record
    return render_template("transaction.html", result=result)

@app.route("/ledger")
def ledger():
    chain = read_json(LEDGER_FILE)
    return render_template("ledger.html", ledger=chain)

@app.route("/kyc_status", methods=["GET", "POST"])
def kyc_status():
    user = None
    if request.method == "POST":
        user_id = request.form["user_id"]
        users = read_json(KYC_FILE)
        for u in users:
            if u["user_id"] == user_id:
                user = u
                break
    return render_template("kyc_status.html", user=user)
    
if __name__ == "__main__":
    app.run(debug=True)
