"""
Dataset Upload & Processing Blueprint
Handles CSV file uploads, schema validation, data cleaning, preview table generation,
and database ingestion for ML predictions.
"""

import os
import io
from flask import Blueprint, render_template, request, flash, session, redirect, url_for, Response
from werkzeug.utils import secure_filename
from models import db, User, EnergyRecord
from routes.auth import login_required
from ml.preprocessing import validate_uploaded_csv, TARGET_COLUMN

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload_view():
    """Upload dataset view."""
    user_id = session["user_id"]
    user = db.session.get(User, user_id)
    currency = user.currency if user else "₹"
    tariff = user.default_tariff if user else 8.0

    preview_stats = None
    preview_rows = None

    if request.method == "POST":
        if "file" not in request.files:
            flash("No file selected. Please choose a CSV dataset file.", "danger")
            return redirect(request.url)

        file = request.files["file"]

        if file.filename == "":
            flash("No file selected.", "danger")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file format. Only .CSV files are accepted.", "danger")
            return redirect(request.url)

        # Secure and save uploaded file
        upload_folder = os.path.join("data", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        filename = secure_filename(f"user_{user_id}_{file.filename}")
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # Validate and clean CSV
        is_valid, msg, stats, cleaned_df = validate_uploaded_csv(file_path)

        if not is_valid:
            flash(f"CSV Validation Failed: {msg}", "danger")
            # Remove invalid file
            if os.path.exists(file_path):
                os.remove(file_path)
            return render_template("upload.html", currency=currency, tariff=tariff)

        # Ingest cleaned records into User Energy Records database
        try:
            records_to_insert = []
            for _, row in cleaned_df.iterrows():
                consumption_val = float(row.get(TARGET_COLUMN, row.get("consumption", 2.5)))
                cost_val = round(consumption_val * tariff, 2)
                
                rec = EnergyRecord(
                    user_id=user_id,
                    date=str(row.get("date", "2024-06-01")),
                    time=str(row.get("time", f"{int(row.get('hour', 12)):02d}:00")),
                    hour=int(row.get("hour", 12)),
                    consumption=consumption_val,
                    temperature=float(row.get("temperature", 28.0)),
                    humidity=float(row.get("humidity", 55.0)),
                    people=int(row.get("number_of_people", 2)),
                    appliance=str(row.get("appliance_usage", "Uploaded Appliance")),
                    cost=cost_val,
                    source=f"upload_{filename}"
                )
                records_to_insert.append(rec)

            db.session.bulk_save_objects(records_to_insert)
            db.session.commit()

            flash(f"Success! {stats['total_rows']} energy consumption records processed and saved to your account.", "success")
            preview_stats = stats
            preview_rows = stats.get("preview_data", [])

        except Exception as e:
            db.session.rollback()
            flash(f"Database error during ingestion: {str(e)}", "danger")

    return render_template(
        "upload.html",
        currency=currency,
        tariff=tariff,
        stats=preview_stats,
        rows=preview_rows
    )

@upload_bp.route("/download-sample-csv")
def download_sample_csv():
    """Generates and serves a downloadable sample CSV template."""
    csv_content = """date,time,temperature,humidity,number_of_people,appliance_usage,previous_consumption,energy_consumption
2024-07-01,08:00,28.5,62.0,3,Medium,3.2,4.5
2024-07-01,12:00,32.0,55.0,2,Low,4.5,3.8
2024-07-01,18:00,31.5,68.0,4,High,3.8,7.9
2024-07-01,20:00,30.0,72.0,4,High,7.9,8.4
2024-07-01,23:00,27.0,75.0,3,Low,8.4,2.8
2024-07-02,08:00,29.0,60.0,3,Medium,2.8,4.6
2024-07-02,12:00,33.5,50.0,2,Medium,4.6,4.1
2024-07-02,19:00,32.0,65.0,4,High,4.1,8.2
2024-07-02,21:00,30.5,70.0,4,High,8.2,7.8
2024-07-02,23:00,27.5,74.0,3,Low,7.8,2.7
"""
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=sample_energy_data.csv"}
    )
