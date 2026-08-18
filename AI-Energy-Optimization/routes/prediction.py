"""
Prediction Blueprint
Handles manual user inputs, calls ML inference pipeline, renders result cards,
and saves prediction history to SQLite.
"""

from flask import Blueprint, render_template, request, flash, session, jsonify
from models import db, User, Prediction, Alert
from routes.auth import login_required
from ml.prediction import predict_energy_consumption
from datetime import datetime
import json

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route("/predict", methods=["GET", "POST"])
@login_required
def predict_view():
    """Predict energy consumption interactive view."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    currency = user.currency if user else "₹"
    tariff = user.default_tariff if user else 8.0

    # Default Form Values
    now = datetime.now()
    default_form = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M"),
        "temperature": 30.5,
        "humidity": 62.0,
        "people": 3,
        "appliance_usage": "Medium",
        "previous_consumption": 4.2
    }

    result = None

    if request.method == "POST":
        date_str = request.form.get("date", default_form["date"]).strip()
        time_str = request.form.get("time", default_form["time"]).strip()
        temp_str = request.form.get("temperature", "30.0").strip()
        humidity_str = request.form.get("humidity", "60.0").strip()
        people_str = request.form.get("people", "2").strip()
        appliance_usage = request.form.get("appliance_usage", "Medium").strip()
        prev_kwh_str = request.form.get("previous_consumption", "3.5").strip()

        # Input Validation & Sanitization
        errors = []
        try:
            temp = float(temp_str)
            if not (-10.0 <= temp <= 60.0):
                errors.append("Temperature must be between -10°C and 60°C.")
        except ValueError:
            errors.append("Please enter a valid numeric temperature.")
            temp = 30.0

        try:
            humidity = float(humidity_str)
            if not (0.0 <= humidity <= 100.0):
                errors.append("Humidity must be between 0% and 100%.")
        except ValueError:
            errors.append("Please enter a valid numeric humidity percentage.")
            humidity = 60.0

        try:
            people = int(people_str)
            if people < 1 or people > 30:
                errors.append("Number of people must be between 1 and 30.")
        except ValueError:
            errors.append("Please enter a valid whole number for occupants.")
            people = 2

        try:
            prev_kwh = float(prev_kwh_str)
            if prev_kwh < 0:
                errors.append("Previous energy consumption cannot be negative.")
        except ValueError:
            errors.append("Please enter a valid numeric previous consumption.")
            prev_kwh = 3.5

        if appliance_usage not in ["Low", "Medium", "High"]:
            appliance_usage = "Medium"

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template(
                "prediction.html",
                currency=currency,
                tariff=tariff,
                form=request.form,
                result=None
            )

        try:
            # Execute ML Inference
            result = predict_energy_consumption(
                date=date_str,
                time=time_str,
                temperature=temp,
                humidity=humidity,
                number_of_people=people,
                appliance_usage=appliance_usage,
                previous_consumption=prev_kwh,
                tariff_per_kwh=tariff,
                currency=currency
            )

            # Save prediction to SQLite database
            hour_val = int(time_str.split(":")[0]) if ":" in time_str else 12
            rec_json = json.dumps(result["recommendations"])

            new_prediction = Prediction(
                user_id=user_id,
                date=date_str,
                time=time_str,
                hour=hour_val,
                temperature=temp,
                humidity=humidity,
                people=people,
                appliance_usage=appliance_usage,
                previous_consumption=prev_kwh,
                predicted_consumption=result["predicted_kwh"],
                estimated_cost=result["estimated_cost"],
                category=result["category"],
                recommendations_json=rec_json
            )
            db.session.add(new_prediction)

            # If prediction is High category, raise an alert
            if result["category"] == "High":
                alert = Alert(
                    user_id=user_id,
                    alert_type="warning",
                    title="High Consumption Predicted!",
                    message=f"Prediction on {date_str} at {time_str} is {result['predicted_kwh']} kWh. Consider applying the recommended energy conservation measures."
                )
                db.session.add(alert)

            db.session.commit()
            flash(f"Energy Prediction Computed: {result['predicted_kwh']} kWh ({currency}{result['estimated_cost']})", "success")

            return render_template(
                "prediction.html",
                currency=currency,
                tariff=tariff,
                form=request.form,
                result=result
            )

        except Exception as e:
            db.session.rollback()
            flash(f"Prediction Error: {str(e)}", "danger")
            return render_template(
                "prediction.html",
                currency=currency,
                tariff=tariff,
                form=request.form,
                result=None
            )

    return render_template(
        "prediction.html",
        currency=currency,
        tariff=tariff,
        form=default_form,
        result=None
    )

@prediction_bp.route("/api/predict", methods=["POST"])
@login_required
def api_predict():
    """AJAX JSON Prediction endpoint."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    currency = user.currency if user else "₹"
    tariff = user.default_tariff if user else 8.0

    data = request.get_json(silent=True) or {}
    
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    time_str = data.get("time", "12:00")
    temp = float(data.get("temperature", 30.0))
    humidity = float(data.get("humidity", 60.0))
    people = int(data.get("people", 2))
    appliance_usage = data.get("appliance_usage", "Medium")
    prev_kwh = float(data.get("previous_consumption", 3.5))

    try:
        result = predict_energy_consumption(
            date=date_str,
            time=time_str,
            temperature=temp,
            humidity=humidity,
            number_of_people=people,
            appliance_usage=appliance_usage,
            previous_consumption=prev_kwh,
            tariff_per_kwh=tariff,
            currency=currency
        )
        return jsonify({"success": True, "data": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
