"""
History & Data Management Blueprint
Provides search, filtering, pagination, CSV export, and deletion of energy records and prediction logs.
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, Response
from models import db, User, EnergyRecord, Prediction
from routes.auth import login_required
import csv
import io

history_bp = Blueprint("history", __name__)

@history_bp.route("/history")
@login_required
def history_view():
    """Renders user consumption history and ML prediction logs."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    currency = user.currency if user else "₹"

    tab = request.args.get("tab", "records")
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # Query Energy Records
    records_pagination = EnergyRecord.query.filter_by(user_id=user_id)\
        .order_by(EnergyRecord.date.desc(), EnergyRecord.hour.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    # Query Predictions
    predictions_pagination = Prediction.query.filter_by(user_id=user_id)\
        .order_by(Prediction.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    total_records = EnergyRecord.query.filter_by(user_id=user_id).count()
    total_predictions = Prediction.query.filter_by(user_id=user_id).count()

    return render_template(
        "history.html",
        currency=currency,
        tab=tab,
        records=records_pagination.items,
        records_pagination=records_pagination,
        predictions=predictions_pagination.items,
        predictions_pagination=predictions_pagination,
        total_records=total_records,
        total_predictions=total_predictions
    )

@history_bp.route("/history/export-csv")
@login_required
def export_csv():
    """Generates and streams a CSV export of all user energy records."""
    user_id = session["user_id"]
    records = EnergyRecord.query.filter_by(user_id=user_id).order_by(EnergyRecord.date.asc(), EnergyRecord.hour.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    
    # Headers
    writer.writerow([
        "Record_ID", "Date", "Time", "Hour", "Consumption_kWh",
        "Temperature_C", "Humidity_Pct", "Occupants", "Appliance", "Cost", "Source", "Logged_At"
    ])

    for r in records:
        writer.writerow([
            r.id, r.date, r.time, r.hour, r.consumption,
            r.temperature, r.humidity, r.people, r.appliance, r.cost, r.source, r.created_at
        ])

    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=energy_history_user_{user_id}.csv"}
    )

@history_bp.route("/history/delete-record/<int:record_id>", methods=["POST"])
@login_required
def delete_record(record_id):
    """Deletes an energy record owned by current user."""
    user_id = session["user_id"]
    record = EnergyRecord.query.filter_by(id=record_id, user_id=user_id).first_or_404()
    
    db.session.delete(record)
    db.session.commit()
    flash(f"Record #{record_id} deleted successfully.", "success")
    return redirect(url_for("history.history_view", tab="records"))

@history_bp.route("/history/delete-prediction/<int:pred_id>", methods=["POST"])
@login_required
def delete_prediction(pred_id):
    """Deletes a prediction log owned by current user."""
    user_id = session["user_id"]
    pred = Prediction.query.filter_by(id=pred_id, user_id=user_id).first_or_404()
    
    db.session.delete(pred)
    db.session.commit()
    flash(f"Prediction log #{pred_id} deleted successfully.", "success")
    return redirect(url_for("history.history_view", tab="predictions"))
