import json  # Import JSON to handle specs properly
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.models import db, Product, Category

product_bp = Blueprint("product", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@product_bp.route("/add_product", methods=["POST"])
def add_product():
    try:
        # Get Form Data
        category_id = request.form.get("category_id")
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        specs = request.form.get("specs")

        # Validate Required Fields (Ensure they are not empty or None)
        if not category_id or not name or not description or not price or not specs:
            return jsonify({"message": "All fields are required! Missing data."}), 400
        
        # Validate category
        category = Category.query.get(category_id)
        if not category:
            return jsonify({"message": "Invalid category selected!"}), 400

        # Ensure `specs` is valid JSON
        try:
            specs = json.loads(specs) if specs else {}
        except json.JSONDecodeError:
            return jsonify({"message": "Invalid JSON format for specs!"}), 400

        # Validate price (ensure it's a valid number)
        try:
            price = float(price)
            if price <= 0:
                return jsonify({"message": "Price must be greater than 0!"}), 400
        except ValueError:
            return jsonify({"message": "Invalid price value!"}), 400

        # Handle Image Uploads
        image_urls = []
        if "images" in request.files:
            images = request.files.getlist("images")
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                    image.save(filepath)
                    image_urls.append(f"/static/uploads/{filename}")

        # Handle Video Upload
        video_url = ""
        if "video" in request.files:
            video = request.files["video"]
            if video and allowed_file(video.filename):
                filename = secure_filename(video.filename)
                filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
                video.save(filepath)
                video_url = f"/static/uploads/{filename}"

        # Convert list of images to a comma-separated string
        image_urls_str = ",".join(image_urls) if image_urls else ""

        # Create new product
        new_product = Product(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            specs=specs,
            image_urls=image_urls_str,
            video_url=video_url
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            "message": "Product added successfully!",
            "product": {
                "id": new_product.id,
                "category_id": new_product.category_id,
                "name": new_product.name,
                "description": new_product.description,
                "price": new_product.price,
                "specs": new_product.specs,
                "image_urls": new_product.image_urls.split(",") if new_product.image_urls else [],
                "video_url": new_product.video_url
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


