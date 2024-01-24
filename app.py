import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

#db = SQL(os.getenv("DATABASE_URL", "sqlite:///database.db"))

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]

    if request.method == "POST":
        note = request.form.get("note")

        if not note:
            flash("Please enter note!", category="error")

        db.execute("INSERT INTO notes (user_id, data) VALUES(?, ?)", user_id, note)

        return redirect("/")

    notes = db.execute("SELECT * FROM notes WHERE user_id = ?", user_id)
    return render_template("index.html", notes=notes)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        if not email:
            flash("Please enter email!", category="error")
        elif not password:
            flash("Please enter password!", category="error")

        elif len(rows) != 1 or rows[0]["email"] != email:
            flash("Email does not exist! Please enter a new email.", category="error")
        elif not check_password_hash(rows[0]["password"], password):
            flash(
                "Invalid password! Please enter a correct password.", category="error"
            )
        else:
            flash("Logged in succefully!", category="success")

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Handle successful login attempts
            return redirect("/")

        # Handle unsuccessful login attempts
        return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password != confirmation:
            flash("Passwords don't match.", category="error")
        elif len(confirmation) < 7:
            flash("Password must be at least 7 characters.", category="error")
        else:
            # Check if the email already exists in the database
            rows = db.execute("SELECT * FROM users WHERE email = ?", email)

            if len(rows) > 0:
                flash(
                    "Email already exists! Enter a different email address.",
                    category="error",
                )
            else:
                hashed_password = generate_password_hash(password)
                db.execute(
                    "INSERT INTO users (email, password, first_name) VALUES (?, ?, ?)",
                    email,
                    hashed_password,
                    first_name,
                )
                flash("Account created!", category="success")
                return redirect("/")

    return render_template("sign_up.html")


@app.route("/delete", methods=["POST"])
@login_required
def delete_note():
    user_id = session["user_id"]
    id = request.form.get("id")

    if id:
        db.execute("DELETE FROM notes WHERE id = ? AND user_id = ?", id, user_id)
        flash("Note deleted successfully", category="success")
    return redirect("/")
