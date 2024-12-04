from flask import Flask, render_template, request, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Global variable to track the current user's account
current_account = None

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/new-customer", methods=["GET", "POST"])
def new_customer():
    if request.method == "POST":
        name = request.form["name"]
        account_number = request.form["account_number"]
        balance = request.form["balance"]

        customers = {}
        if os.path.exists("customers.json"):
            with open("customers.json") as file:
                customers = json.load(file)

        if account_number in customers:
            flash("Account number already exists!")
            return render_template("new_customer.html")

        customers[account_number] = {"name": name, "balance": float(balance)}

        with open("customers.json", "w") as file:
            json.dump(customers, file)

        flash("Account created successfully!")
        return render_template("home.html")
    return render_template("new_customer.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    global current_account
    if request.method == "POST":
        account_number = request.form["account_number"]

        if os.path.exists("customers.json"):
            with open("customers.json") as file:
                customers = json.load(file)

            if account_number in customers:
                current_account = account_number
                customer = customers[account_number]
                return render_template(
                    "transaction.html", name=customer["name"], balance=customer["balance"]
                )

        flash("Invalid account number!")
        return render_template("login.html")
    return render_template("login.html")

@app.route("/transactions", methods=["POST"])
def transactions():
    global current_account
    if not current_account:
        return render_template("home.html")

    option = request.form["option"]
    amount = float(request.form["amount"])

    if os.path.exists("customers.json"):
        with open("customers.json") as file:
            customers = json.load(file)

        if current_account in customers:
            customer = customers[current_account]

            if option == "deposit":
                customer["balance"] += amount
                flash(f"Deposited GH₵ {amount:.2f} successfully!")

            elif option == "withdraw":
                if customer["balance"] >= amount:
                    customer["balance"] -= amount
                    flash(f"Withdrawn GH₵ {amount:.2f} successfully!")
                else:
                    flash("Insufficient balance!")

            elif option == "loan":
                interest = amount * 0.1
                customer["balance"] += amount
                flash(f"Loan of GH₵ {amount:.2f} taken successfully!")
                flash(f"Interest to be paid: GH₵ {interest:.2f}")

            with open("customers.json", "w") as file:
                json.dump(customers, file)

            return render_template(
                "transaction.html", name=customer["name"], balance=customer["balance"]
            )
    return render_template("home.html")

if __name__ == "__main__":
    app.run(port=5055)
