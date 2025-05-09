from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models.models import db, ContactMessage
from flask import send_file
import pandas as pd
from io import BytesIO
from datetime import datetime

contact_bp = Blueprint("contact_bp", __name__)

# Limiter object (to be initialized in app factory)
limiter = Limiter(get_remote_address, default_limits=["200 per day", "50 per hour"])

# Limit contact submissions: 4 per hour per IP
@contact_bp.route("/contact", methods=["GET", "POST"])
@limiter.limit("4 per hour")
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        city = request.form.get("city")
        state = request.form.get("state")
        requirement = request.form.get("requirement")
        message = request.form.get("message")
        ip_address = request.remote_addr

        new_message = ContactMessage(
            name=name,
            email=email,
            phone=phone,
            city=city,
            state=state,
            requirement=requirement,
            message=message,
            ip_address=ip_address
        )

        db.session.add(new_message)
        db.session.commit()
        flash("Your message has been sent successfully!")

        return redirect(url_for("index"))

    return render_template("index.html")


#DEV: code for admin panel for user contact details..
@contact_bp.route("/admin/contacts", methods=["GET", "POST"])
def admin_contacts():
    filter_date = request.args.get("date")
    query = ContactMessage.query

    if filter_date:
        try:
            filter_obj = datetime.strptime(filter_date, "%Y-%m-%d").date()
            query = query.filter(ContactMessage.created_at.cast(db.Date) == filter_obj)
        except ValueError:
            flash("Invalid date format. Use YYYY-MM-DD.", "error")

    messages = query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("contact-admin.html", messages=messages)

@contact_bp.route("/admin/contacts/delete", methods=["POST"])
def delete_contacts():
    ids = request.form.getlist("selected_ids")
    if ids:
        ContactMessage.query.filter(ContactMessage.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        flash(f"Deleted {len(ids)} messages.", "success")
    return redirect(url_for("contact_bp.admin_contacts"))

@contact_bp.route("/admin/contacts/download", methods=["GET"])
def download_contacts():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    data = [{
        "ID": msg.id,
        "Name": msg.name,
        "Email": msg.email,
        "Phone": msg.phone,
        "City": msg.city,
        "State": msg.state,
        "Requirement": msg.requirement,
        "Message": msg.message,
        "IP Address": msg.ip_address,
        "Submitted At": msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]

    df = pd.DataFrame(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Contact Messages")
    output.seek(0)

    return send_file(output, download_name="contact_messages.xlsx", as_attachment=True)
# ...................................................