"""
Settings Blueprint
Manages user profile, tariff defaults, currency, alert preferences, and password updates.
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models import db, User, UserSetting, Alert
from routes.auth import login_required

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings_view():
    """Settings and preferences view."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    user_setting = UserSetting.query.filter_by(user_id=user_id).first()

    if not user_setting:
        user_setting = UserSetting(user_id=user_id, default_tariff=user.default_tariff, currency=user.currency)
        db.session.add(user_setting)
        db.session.commit()

    if request.method == "POST":
        action = request.form.get("action")

        if action == "update_profile":
            name = request.form.get("name", "").strip()
            currency = request.form.get("currency", "₹").strip()
            tariff_str = request.form.get("default_tariff", "8.0").strip()

            if not name:
                flash("Name cannot be blank.", "danger")
            else:
                try:
                    tariff = float(tariff_str)
                    if tariff <= 0:
                        tariff = 8.0
                except ValueError:
                    tariff = 8.0

                user.name = name
                user.currency = currency
                user.default_tariff = tariff
                user_setting.currency = currency
                user_setting.default_tariff = tariff

                session["user_name"] = user.name
                session["currency"] = user.currency
                session["tariff"] = user.default_tariff

                db.session.commit()
                flash("Profile and energy preferences updated successfully.", "success")

        elif action == "change_password":
            current_password = request.form.get("current_password", "")
            new_password = request.form.get("new_password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not user.check_password(current_password):
                flash("Current password is incorrect.", "danger")
            elif len(new_password) < 6:
                flash("New password must be at least 6 characters.", "danger")
            elif new_password != confirm_password:
                flash("New passwords do not match.", "danger")
            else:
                user.set_password(new_password)
                db.session.commit()
                flash("Password updated successfully.", "success")

        elif action == "clear_alerts":
            Alert.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            flash("All energy alert notifications cleared.", "info")

        return redirect(url_for("settings.settings_view"))

    return render_template(
        "settings.html",
        user=user,
        settings=user_setting
    )
