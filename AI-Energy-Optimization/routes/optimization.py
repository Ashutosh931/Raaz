"""
Optimization Blueprint
Presents dynamic energy conservation advice and the interactive Energy Saving Simulator.
"""

from flask import Blueprint, render_template, request, session, jsonify
from models import db, User, EnergyRecord, Prediction
from routes.auth import login_required
from ml.optimization import generate_smart_recommendations, EnergySavingSimulator
import pandas as pd
from datetime import datetime

optimization_bp = Blueprint("optimization", __name__)

@optimization_bp.route("/optimization")
@login_required
def optimization_view():
    """Renders energy optimization insights and interactive simulator."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    currency = user.currency if user else "₹"
    tariff = user.default_tariff if user else 8.0

    # Retrieve recent consumption data for user
    records = EnergyRecord.query.filter_by(user_id=user_id).all()
    latest_pred = Prediction.query.filter_by(user_id=user_id).order_by(Prediction.created_at.desc()).first()

    if records:
        df = pd.DataFrame([{
            "consumption": r.consumption,
            "temperature": r.temperature if r.temperature is not None else 30.0,
            "humidity": r.humidity if r.humidity is not None else 60.0,
            "hour": r.hour
        } for r in records])

        avg_daily_kwh = float(df["consumption"].sum()) / max(1.0, len(df["consumption"]) / 24.0)
        baseline_monthly_kwh = round(avg_daily_kwh * 30.0, 1)
        avg_temp = float(df["temperature"].mean())
        avg_hum = float(df["humidity"].mean())
        peak_hour_avg = float(df[df["hour"].between(18, 22)]["consumption"].mean()) if not df[df["hour"].between(18, 22)].empty else 6.5
    else:
        baseline_monthly_kwh = 240.0
        avg_temp = 31.0
        avg_hum = 65.0
        peak_hour_avg = 6.2

    # Dynamic recommendations tailored to user's context
    current_hour = datetime.now().hour
    recommendations = generate_smart_recommendations(
        hour=current_hour,
        temperature=round(avg_temp, 1),
        humidity=round(avg_hum, 1),
        people=3,
        appliance_level="high" if peak_hour_avg > 5.5 else "medium",
        predicted_kwh=round(peak_hour_avg, 2),
        tariff=tariff,
        currency=currency
    )

    # Initial Simulation calculation
    initial_simulation = EnergySavingSimulator.calculate_simulation(
        baseline_monthly_kwh=baseline_monthly_kwh,
        tariff_per_kwh=tariff,
        reduce_ac_pct=15.0,
        reduce_lighting_pct=20.0,
        reduce_appliances_pct=10.0,
        shift_peak_pct=25.0,
        eliminate_standby=True
    )

    return render_template(
        "optimization.html",
        currency=currency,
        tariff=tariff,
        baseline_monthly_kwh=baseline_monthly_kwh,
        recommendations=recommendations,
        initial_sim=initial_simulation
    )

@optimization_bp.route("/api/simulate-savings", methods=["POST"])
@login_required
def simulate_savings_api():
    """Calculates simulator projections reactively upon slider changes."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    tariff_default = user.default_tariff if user else 8.0

    data = request.get_json(silent=True) or {}

    baseline_monthly_kwh = float(data.get("baseline_monthly_kwh", 240.0))
    tariff = float(data.get("tariff", tariff_default))
    reduce_ac_pct = float(data.get("reduce_ac_pct", 0.0))
    reduce_lighting_pct = float(data.get("reduce_lighting_pct", 0.0))
    reduce_appliances_pct = float(data.get("reduce_appliances_pct", 0.0))
    shift_peak_pct = float(data.get("shift_peak_pct", 0.0))
    eliminate_standby = bool(data.get("eliminate_standby", False))

    sim_result = EnergySavingSimulator.calculate_simulation(
        baseline_monthly_kwh=baseline_monthly_kwh,
        tariff_per_kwh=tariff,
        reduce_ac_pct=reduce_ac_pct,
        reduce_lighting_pct=reduce_lighting_pct,
        reduce_appliances_pct=reduce_appliances_pct,
        shift_peak_pct=shift_peak_pct,
        eliminate_standby=eliminate_standby
    )

    return jsonify({"success": True, "data": sim_result})
