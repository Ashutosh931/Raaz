"""
Electricity Cost Calculator Blueprint
Calculates daily, weekly, monthly, and tiered billing costs with customizable currency and tariffs.
"""

from flask import Blueprint, render_template, request, session, flash
from models import db, User
from routes.auth import login_required

cost_calculator_bp = Blueprint("cost_calculator", __name__)

def calculate_tiered_cost(monthly_kwh: float, base_tariff: float) -> dict:
    """
    Calculates electricity bill based on standard progressive utility tier slabs:
    - Tier 1: First 100 kWh @ 60% of base tariff (Lifeline block)
    - Tier 2: Next 200 kWh (101 - 300 kWh) @ 100% of base tariff
    - Tier 3: Above 300 kWh @ 135% of base tariff (Heavy consumption surcharge)
    """
    kwh = max(0.0, monthly_kwh)
    t1_rate = round(base_tariff * 0.60, 2)
    t2_rate = round(base_tariff * 1.00, 2)
    t3_rate = round(base_tariff * 1.35, 2)

    tier1_kwh = min(100.0, kwh)
    tier1_cost = tier1_kwh * t1_rate

    rem_after_t1 = max(0.0, kwh - 100.0)
    tier2_kwh = min(200.0, rem_after_t1)
    tier2_cost = tier2_kwh * t2_rate

    tier3_kwh = max(0.0, rem_after_t1 - 200.0)
    tier3_cost = tier3_kwh * t3_rate

    total_cost = tier1_cost + tier2_cost + tier3_cost

    return {
        "tier1": {"range": "0 - 100 kWh", "rate": t1_rate, "kwh": round(tier1_kwh, 1), "cost": round(tier1_cost, 2)},
        "tier2": {"range": "101 - 300 kWh", "rate": t2_rate, "kwh": round(tier2_kwh, 1), "cost": round(tier2_cost, 2)},
        "tier3": {"range": "> 300 kWh", "rate": t3_rate, "kwh": round(tier3_kwh, 1), "cost": round(tier3_cost, 2)},
        "total_cost": round(total_cost, 2),
        "effective_rate": round(total_cost / max(1.0, kwh), 2)
    }

@cost_calculator_bp.route("/cost-calculator", methods=["GET", "POST"])
@login_required
def cost_calculator_view():
    """Electricity cost calculator view."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    default_currency = user.currency if user else "₹"
    default_tariff = user.default_tariff if user else 8.0

    # Defaults
    consumption_kwh = 10.0
    calc_type = "daily"  # 'daily' or 'monthly'
    tariff = default_tariff
    currency = default_currency

    calc_result = None

    if request.method == "POST":
        try:
            consumption_kwh = float(request.form.get("consumption_kwh", 10.0))
            tariff = float(request.form.get("tariff", default_tariff))
            calc_type = request.form.get("calc_type", "daily")
            currency = request.form.get("currency", default_currency).strip()

            if consumption_kwh < 0:
                flash("Consumption cannot be negative.", "danger")
                consumption_kwh = 10.0

            if tariff <= 0:
                flash("Tariff must be a positive number.", "danger")
                tariff = 8.0

            # Compute Daily, Weekly, Monthly, Yearly projections
            if calc_type == "daily":
                daily_kwh = consumption_kwh
                monthly_kwh = daily_kwh * 30.0
            else:
                monthly_kwh = consumption_kwh
                daily_kwh = monthly_kwh / 30.0

            weekly_kwh = daily_kwh * 7.0
            yearly_kwh = monthly_kwh * 12.0

            # Flat Rate Calculations
            daily_cost = round(daily_kwh * tariff, 2)
            weekly_cost = round(weekly_kwh * tariff, 2)
            monthly_cost = round(monthly_kwh * tariff, 2)
            yearly_cost = round(yearly_kwh * tariff, 2)

            # Tiered Slab Calculations
            tiered_data = calculate_tiered_cost(monthly_kwh, tariff)

            # Savings scenarios
            save_10_cost = round(monthly_cost * 0.10, 2)
            save_20_cost = round(monthly_cost * 0.20, 2)
            save_30_cost = round(monthly_cost * 0.30, 2)

            calc_result = {
                "daily_kwh": round(daily_kwh, 2),
                "weekly_kwh": round(weekly_kwh, 2),
                "monthly_kwh": round(monthly_kwh, 2),
                "yearly_kwh": round(yearly_kwh, 2),
                "daily_cost": daily_cost,
                "weekly_cost": weekly_cost,
                "monthly_cost": monthly_cost,
                "yearly_cost": yearly_cost,
                "tariff": tariff,
                "currency": currency,
                "tiered": tiered_data,
                "savings": {
                    "save_10_pct": save_10_cost,
                    "save_20_pct": save_20_cost,
                    "save_30_pct": save_30_cost
                }
            }

        except ValueError:
            flash("Invalid input values. Please enter numeric values.", "danger")

    if calc_result is None:
        # Default initial calculation
        daily_kwh = 8.0
        monthly_kwh = daily_kwh * 30.0
        calc_result = {
            "daily_kwh": daily_kwh,
            "weekly_kwh": daily_kwh * 7.0,
            "monthly_kwh": monthly_kwh,
            "yearly_kwh": monthly_kwh * 12.0,
            "daily_cost": round(daily_kwh * default_tariff, 2),
            "weekly_cost": round(daily_kwh * 7.0 * default_tariff, 2),
            "monthly_cost": round(monthly_kwh * default_tariff, 2),
            "yearly_cost": round(monthly_kwh * 12.0 * default_tariff, 2),
            "tariff": default_tariff,
            "currency": default_currency,
            "tiered": calculate_tiered_cost(monthly_kwh, default_tariff),
            "savings": {
                "save_10_pct": round(monthly_kwh * default_tariff * 0.10, 2),
                "save_20_pct": round(monthly_kwh * default_tariff * 0.20, 2),
                "save_30_pct": round(monthly_kwh * default_tariff * 0.30, 2)
            }
        }

    return render_template(
        "cost_calculator.html",
        currency=currency,
        tariff=tariff,
        consumption_kwh=consumption_kwh,
        calc_type=calc_type,
        result=calc_result
    )
