from flask import Blueprint, render_template
from models.models import Category, Product

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_panel():
    categories = Category.query.all()
    products = Product.query.all()
    return render_template("admin.html", categories=categories, products=products)


