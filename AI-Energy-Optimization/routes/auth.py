"""
Authentication Blueprint
Handles user registration, secure login, password hashing, and session management.
"""

from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, g
from models import db, User, UserSetting, Alert, EnergyRecord
import pandas as pd
import os
from datetime import datetime, timedelta
import random

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    """Decorator to require login for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def seed_initial_user_data(user_id: int):
    """Seeds initial sample energy records for newly registered user so dashboard is immediately populated."""
    try:
        dataset_path = "data/energy_consumption.csv"
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
            # Pick last 7 days of records (168 hourly rows)
            sample_df = df.tail(168)
            for _, row in sample_df.iterrows():
                rec = EnergyRecord(
                    user_id=user_id,
                    date=str(row.get("date")),
                    time=str(row.get("time", "12:00")),
                    hour=int(row.get("hour", 12)),
                    consumption=float(row.get("energy_consumption", 2.5)),
                    temperature=float(row.get("temperature", 28.0)),
                    humidity=float(row.get("humidity", 55.0)),
                    people=int(row.get("number_of_people", 2)),
                    appliance=str(row.get("appliance_usage", "Medium")),
                    cost=round(float(row.get("energy_consumption", 2.5)) * 8.0, 2),
                    source="initial_seed"
                )
                db.session.add(rec)
            db.session.commit()
    except Exception as e:
        print(f"Error seeding user data: {e}")
        db.session.rollback()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration route."""
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard_view"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        currency = request.form.get("currency", "₹").strip()
        tariff_str = request.form.get("tariff", "8.0").strip()

        # Validation
        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return render_template("register.html", name=name, email=email)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("register.html", name=name, email=email)

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", name=name, email=email)

        try:
            tariff = float(tariff_str)
            if tariff <= 0:
                tariff = 8.0
        except ValueError:
            tariff = 8.0

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email address already exists. Please log in.", "warning")
            return redirect(url_for("auth.login"))

        # Create new user
        new_user = User(
            name=name,
            email=email,
            currency=currency,
            default_tariff=tariff
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()  # to get new_user.id

        # Create User Settings
        user_settings = UserSetting(
            user_id=new_user.id,
            default_tariff=tariff,
            currency=currency,
            dark_mode=False
        )
        db.session.add(user_settings)

        # Welcome Alert
        welcome_alert = Alert(
            user_id=new_user.id,
            alert_type="success",
            title="Welcome to AI Energy Optimizer!",
            message="Your account is configured. Check your dashboard to view smart energy predictions and cost-saving insights."
        )
        db.session.add(welcome_alert)
        db.session.commit()

        # Seed initial energy history records
        seed_initial_user_data(new_user.id)

        # Log user in
        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_email"] = new_user.email
        session["currency"] = new_user.currency
        session["tariff"] = new_user.default_tariff

        flash(f"Welcome, {new_user.name}! Your account was created successfully.", "success")
        return redirect(url_for("dashboard.dashboard_view"))

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login route."""
    if "user_id" in session:
        return redirect(url_for("dashboard.dashboard_view"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        next_url = request.args.get("next")

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html", email=email)

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_email"] = user.email
            session["currency"] = user.currency
            session["tariff"] = user.default_tariff

            flash(f"Welcome back, {user.name}!", "success")
            if next_url and next_url.startswith("/"):
                return redirect(next_url)
            return redirect(url_for("dashboard.dashboard_view"))
        else:
            flash("Invalid email address or password. Please try again.", "danger")
            return render_template("login.html", email=email)

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    """User logout route."""
    user_name = session.get("user_name", "User")
    session.clear()
    flash(f"You have been logged out successfully. Have a great day, {user_name}!", "info")
    return redirect(url_for("auth.login"))
