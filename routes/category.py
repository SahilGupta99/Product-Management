from flask import Blueprint, request, jsonify, render_template, json, current_app as app
from models.models import db, Category, Product
import os
import time
from werkzeug.utils import secure_filename
category_bp = Blueprint("category", __name__)

# @category_bp.route("/product/<int:product_id>")
# def product_page(product_id):
#     # Get product with 404 handling
#     product = Product.query.get_or_404(product_id)
    
#     # Process product data
#     product_data = {
#         "id": product.id,
#         "name": product.name,
#         "description": product.description,
#         "price": product.price,
#         "category_id": product.category_id,
#         "specs": product.specs or {},  # Directly use JSON field
#         "image_urls": product.image_urls or [],  # Directly use JSON field
#         "video_url": product.video_url
#     }

#     # Get 4 related products from same category
#     related_products = Product.query.filter(
#         Product.category_id == product.category_id,
#         Product.id != product.id
#     ).limit(4).all()

#     # Process related products data
#     related_products_data = []
#     for related in related_products:
#         related_products_data.append({
#             "id": related.id,
#             "name": related.name,
#             "price": related.price,
#             "primary_image": related.image_urls[0] if related.image_urls else None
#         })

#     return render_template(
#         "product-detail.html",
#         product=product_data,
#         related_products=related_products_data,
#         category=product.category  # Pass the category object for breadcrumbs
#     )

@category_bp.route("/product/<int:product_id>")
def product_page(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Process product data same as category route
    if isinstance(product.specs, str):
        try:
            specs = json.loads(product.specs)
        except json.JSONDecodeError:
            app.logger.error(f"Error decoding specs for product {product.id}")
            specs = {}
    else:
        specs = product.specs or {}

    if isinstance(product.image_urls, str):
        try:
            images = json.loads(product.image_urls) if "[" in product.image_urls else product.image_urls.split(",")
        except json.JSONDecodeError:
            app.logger.error(f"Error decoding image_urls for product {product.id}")
            images = []
    else:
        images = product.image_urls or []

    # Get related products
    related_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id
    ).limit(4).all()

    # Process related products same as main products
    related_products_data = []
    for related in related_products:
        related_products_data.append({
            "id": related.id,
            "name": related.name,
            "price": float(related.price) if related.price else 0.0,
            "images": related.image_urls.split(",") if isinstance(related.image_urls, str) else related.image_urls or []
        })

    return render_template(
        "product-detail.html",
        product={
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price) if product.price else 0.0,
            "specs": specs,
            "images": images,
            "video_url": product.video_url,
            "category_id": product.category_id
        },
        related_products=related_products_data,
        category=product.category
    )


# Route for rendering homepage
@category_bp.route("/products")
def index():
    categories = Category.query.all()
    return render_template("product.html", categories=categories)

# Route for displaying category page with products
@category_bp.route("/category/<int:category_id>")
def category_page(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()

    products_data = []
    for product in products:
        app.logger.info(f"Product ID: {product.id}, Specs: {product.specs}, Image URLs: {product.image_urls}")

        # Fix `specs` (Ensure it's valid JSON)
        if isinstance(product.specs, str):
            try:
                specs = json.loads(product.specs)
            except json.JSONDecodeError:
                app.logger.error(f"Error decoding specs for product {product.id}")
                specs = {}
        else:
            specs = product.specs or {}

        # Fix `image_urls` (Ensure it's a valid list)
        if isinstance(product.image_urls, str):
            try:
                images = json.loads(product.image_urls) if "[" in product.image_urls else product.image_urls.split(",")
            except json.JSONDecodeError:
                app.logger.error(f"Error decoding image_urls for product {product.id}")
                images = []
        else:
            images = product.image_urls or []

        products_data.append({
            "id": product.id,
            "name": product.name,
            "description": product.description or "",
            "price": float(product.price) if product.price else 0.0,
            "specs": specs,
            "images": images,
            "video_url": product.video_url or ""
        })

    return render_template(
        "category.html", 
        category=category,  # Pass the entire category object
        products=products_data
    )

# Route for adding a new category (updated to handle image_url)
@category_bp.route("/add_category", methods=["POST"])
def add_category():
    try:
        # Check if request contains files
        if 'image' not in request.files:
            return jsonify({"message": "No image file provided"}), 400
            
        image_file = request.files['image']
        
        # Validate file
        if image_file.filename == '':
            return jsonify({"message": "No selected image file"}), 400
            
        # Validate file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if not ('.' in image_file.filename and 
                image_file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({"message": "Invalid image file type"}), 400

        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            return jsonify({"message": "Category name is required!"}), 400

        # Check for existing category
        if Category.query.filter_by(name=name).first():
            return jsonify({"message": "Category already exists!"}), 400

        # Save the image file
        filename = secure_filename(f"category_{int(time.time())}_{image_file.filename}")
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'categories')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)
        
        # Create relative URL for database
        image_url = f"/static/uploads/categories/{filename}"

        # Create new category
        new_category = Category(
            name=name, 
            description=description,
            image_url=image_url
        )
        db.session.add(new_category)
        db.session.commit()

        return jsonify({
            "message": "Category added successfully!", 
            "category": {
                "id": new_category.id, 
                "name": new_category.name
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding category: {str(e)}")
        return jsonify({"message": "An error occurred while adding the category"}), 500
    

   