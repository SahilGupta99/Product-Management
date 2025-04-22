from flask import Blueprint, request, jsonify, current_app,render_template  # Fixed import - no alias
from models.models import db, Category, Product
import os
import time
from werkzeug.utils import secure_filename
import json  # Added import for json operations

modify_data_bp = Blueprint("modify", __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@modify_data_bp.route('/modify-data')
def modify_data_page():
    # Get all categories to populate dropdowns
    categories = Category.query.all()
    # Get all products (optional - could load via AJAX later)
    products = Product.query.all()
    return render_template('modify-data.html', 
                         categories=categories,
                         products=products)

# Categories Routes
@modify_data_bp.route('/get_categories')
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'description': c.description,
        'image_url': c.image_url
    } for c in categories])

@modify_data_bp.route('/get_category/<int:category_id>')
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'image_url': category.image_url
    })

@modify_data_bp.route('/update_category', methods=['POST'])
def update_category():
    try:
        category_id = request.form.get('id')
        if not category_id:
            return jsonify({'message': 'Category ID is required'}), 400
            
        category = Category.query.get_or_404(category_id)
        category.name = request.form.get('name', category.name)
        category.description = request.form.get('description', category.description)
        
        # Handle image upload if provided
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                if not allowed_file(image_file.filename):
                    return jsonify({'message': 'Invalid file type'}), 400
                    
                filename = secure_filename(f"category_{int(time.time())}_{image_file.filename}")
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'categories')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                image_file.save(filepath)
                category.image_url = f"/static/uploads/categories/{filename}"
        
        db.session.commit()
        return jsonify({'message': 'Category updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating category: {str(e)}")
        return jsonify({'message': 'Failed to update category'}), 500

# ... (rest of your routes remain the same with current_app)

@modify_data_bp.route('/delete_category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Category deleted successfully'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting category: {str(e)}")
        return jsonify({'message': 'Failed to delete category'}), 500

# Products Routes
@modify_data_bp.route('/get_products')
def get_products():
    category_id = request.args.get('category_id')
    query = Product.query.options(db.joinedload(Product.category))  # Eager load category
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    products = query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'price': float(p.price) if p.price else 0.0,
        'category_id': p.category_id,
        'category_name': p.category.name if p.category else 'No Category',
        'images': p.image_urls.split(',') if p.image_urls else []  # Assuming image_urls is comma-separated
    } for p in products])

#DEV: code for delete product 
@modify_data_bp.route('/get_product/<int:product_id>')
def get_product(product_id):
    product = Product.query.options(db.joinedload(Product.category)).get_or_404(product_id)
    
    # Parse specs if they exist
    specs = {}
    if product.specs:
        try:
            specs = json.loads(product.specs) if isinstance(product.specs, str) else product.specs
        except json.JSONDecodeError:
            current_app.logger.error(f"Failed to parse specs for product {product_id}")
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price) if product.price else 0.0,
        'category_id': product.category_id,
        'images': product.image_urls.split(',') if product.image_urls else [],
        'specs': specs
    })

@modify_data_bp.route('/update_product', methods=['POST'])
def update_product():
    try:
        product_id = request.form.get('id')
        if not product_id:
            return jsonify({'message': 'Product ID is required'}), 400
            
        product = Product.query.get_or_404(product_id)
        product.name = request.form.get('name', product.name)
        product.description = request.form.get('description', product.description)
        product.price = request.form.get('price', product.price)
        product.category_id = request.form.get('category_id', product.category_id)
        
        # Handle specs - store as JSON string
        specs = request.form.get('specs')
        if specs:
            try:
                # Validate the specs JSON
                parsed_specs = json.loads(specs)
                product.specs = json.dumps(parsed_specs)  # Store as properly formatted JSON string
            except json.JSONDecodeError as e:
                current_app.logger.error(f"Invalid specs JSON: {str(e)}")
                return jsonify({'message': 'Invalid specifications format'}), 400
        else:
            product.specs = None
        
        # Handle image uploads (existing code remains the same)
        if 'images' in request.files:
            image_files = request.files.getlist('images')
            current_images = product.image_urls.split(',') if product.image_urls else []
            
            for image_file in image_files:
                if image_file.filename != '' and allowed_file(image_file.filename):
                    filename = secure_filename(f"product_{int(time.time())}_{image_file.filename}")
                    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
                    os.makedirs(upload_folder, exist_ok=True)
                    filepath = os.path.join(upload_folder, filename)
                    image_file.save(filepath)
                    current_images.append(f"/static/uploads/products/{filename}")
            
            product.image_urls = ','.join(current_images)
        
        db.session.commit()
        return jsonify({
            'message': 'Product updated successfully',
            'product_id': product.id
        })
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating product: {str(e)}")
        return jsonify({'message': 'Failed to update product'}), 500
    
# @modify_data_bp.route('/get_product/<int:product_id>')
# def get_product(product_id):
#     product = Product.query.options(db.joinedload(Product.category)).get_or_404(product_id)
#     return jsonify({
#         'id': product.id,
#         'name': product.name,
#         'description': product.description,
#         'price': float(product.price) if product.price else 0.0,
#         'category_id': product.category_id,
#         'images': product.image_urls.split(',') if product.image_urls else []
#     })

# #DEV: code for edit or update product 
# @modify_data_bp.route('/update_product', methods=['POST'])
# def update_product():
#     try:
#         product_id = request.form.get('id')
#         if not product_id:
#             return jsonify({'message': 'Product ID is required'}), 400
            
#         product = Product.query.get_or_404(product_id)
#         product.name = request.form.get('name', product.name)
#         product.description = request.form.get('description', product.description)
#         product.price = request.form.get('price', product.price)
#         product.category_id = request.form.get('category_id', product.category_id)
        
#         # Handle specs
#         specs = {}
#         for key in request.form:
#             if key.startswith('spec_'):
#                 spec_name = key[5:]  # Remove 'spec_' prefix
#                 specs[spec_name] = request.form.get(key)
#         product.specs = json.dumps(specs)
        
#         # Handle image uploads
#         if 'images' in request.files:
#             image_files = request.files.getlist('images')
#             current_images = json.loads(product.image_urls) if product.image_urls else []
            
#             for image_file in image_files:
#                 if image_file.filename != '':
#                     filename = secure_filename(f"product_{int(time.time())}_{image_file.filename}")
#                     upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
#                     os.makedirs(upload_folder, exist_ok=True)
#                     filepath = os.path.join(upload_folder, filename)
#                     image_file.save(filepath)
#                     current_images.append(f"/static/uploads/products/{filename}")
            
#             product.image_urls = json.dumps(current_images)
        
#         db.session.commit()
#         return jsonify({'message': 'Product updated successfully'})
        
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error updating product: {str(e)}")
#         return jsonify({'message': 'Failed to update product'}), 500
    
#DEV: code for delete product     
@modify_data_bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting product: {str(e)}")
        return jsonify({'message': 'Failed to delete product'}), 500

@modify_data_bp.route('/remove_product_image/<int:product_id>', methods=['POST'])
def remove_product_image(product_id):
    try:
        data = request.json
        if not data or 'image_url' not in data:
            return jsonify({'message': 'Image URL is required'}), 400
            
        product = Product.query.get_or_404(product_id)
        current_images = json.loads(product.image_urls) if product.image_urls else []
        
        # Remove the image from the list
        updated_images = [img for img in current_images if img != data['image_url']]
        product.image_urls = json.dumps(updated_images)
        
        # Optional: Delete the actual image file
        try:
            if data['image_url'].startswith('/static/uploads/products/'):
                image_path = os.path.join(current_app.root_path, data['image_url'][1:])
                if os.path.exists(image_path):
                    os.remove(image_path)
        except Exception as e:
            current_app.logger.error(f"Error deleting image file: {str(e)}")
        
        db.session.commit()
        return jsonify({'message': 'Image removed successfully'})
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error removing product image: {str(e)}")
        return jsonify({'message': 'Failed to remove image'}), 500



# from flask import Blueprint, request, jsonify, render_template, json, current_app as app
# from models.models import db, Category, Product
# import os
# import time
# from werkzeug.utils import secure_filename
# modify_data_bp = Blueprint("modify", __name__)

# # Categories Routes
# @modify_data_bp.route('/get_categories')
# def get_categories():
#     categories = Category.query.all()
#     return jsonify([{
#         'id': c.id,
#         'name': c.name,
#         'description': c.description,
#         'image_url': c.image_url
#     } for c in categories])

# @modify_data_bp.route('/get_category/<int:category_id>')
# def get_category(category_id):
#     category = Category.query.get_or_404(category_id)
#     return jsonify({
#         'id': category.id,
#         'name': category.name,
#         'description': category.description,
#         'image_url': category.image_url
#     })

# @modify_data_bp.route('/update_category', methods=['POST'])
# def update_category():
#     try:
#         category_id = request.form.get('id')
#         if not category_id:
#             return jsonify({'message': 'Category ID is required'}), 400
            
#         category = Category.query.get_or_404(category_id)
#         category.name = request.form.get('name', category.name)
#         category.description = request.form.get('description', category.description)
        
#         # Handle image upload if provided
#         if 'image' in request.files:
#             image_file = request.files['image']
#             if image_file.filename != '':
#                 filename = secure_filename(f"category_{int(time.time())}_{image_file.filename}")
#                 upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'categories')
#                 os.makedirs(upload_folder, exist_ok=True)
#                 filepath = os.path.join(upload_folder, filename)
#                 image_file.save(filepath)
#                 category.image_url = f"/static/uploads/categories/{filename}"
        
#         db.session.commit()
#         return jsonify({'message': 'Category updated successfully'})
        
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error updating category: {str(e)}")
#         return jsonify({'message': 'Failed to update category'}), 500

# @modify_data_bp.route('/delete_category/<int:category_id>', methods=['DELETE'])
# def delete_category(category_id):
#     try:
#         category = Category.query.get_or_404(category_id)
#         db.session.delete(category)
#         db.session.commit()
#         return jsonify({'message': 'Category deleted successfully'})
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error deleting category: {str(e)}")
#         return jsonify({'message': 'Failed to delete category'}), 500

# # Products Routes
# @modify_data_bp.route('/get_products')
# def get_products():
#     category_id = request.args.get('category_id')
#     query = Product.query
    
#     if category_id:
#         query = query.filter_by(category_id=category_id)
    
#     products = query.all()
#     return jsonify([{
#         'id': p.id,
#         'name': p.name,
#         'description': p.description,
#         'price': float(p.price) if p.price else 0.0,
#         'category_id': p.category_id,
#         'category_name': p.category.name,
#         'images': json.loads(p.image_urls) if p.image_urls else []
#     } for p in products])

# @modify_data_bp.route('/get_product/<int:product_id>')
# def get_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     return jsonify({
#         'id': product.id,
#         'name': product.name,
#         'description': product.description,
#         'price': float(product.price) if product.price else 0.0,
#         'category_id': product.category_id,
#         'images': json.loads(product.image_urls) if product.image_urls else []
#     })

# @modify_data_bp.route('/update_product', methods=['POST'])
# def update_product():
#     try:
#         product_id = request.form.get('id')
#         if not product_id:
#             return jsonify({'message': 'Product ID is required'}), 400
            
#         product = Product.query.get_or_404(product_id)
#         product.name = request.form.get('name', product.name)
#         product.description = request.form.get('description', product.description)
#         product.price = request.form.get('price', product.price)
#         product.category_id = request.form.get('category_id', product.category_id)
        
#         # Handle image uploads if provided
#         if 'images' in request.files:
#             image_files = request.files.getlist('images')
#             current_images = json.loads(product.image_urls) if product.image_urls else []
            
#             for image_file in image_files:
#                 if image_file.filename != '':
#                     filename = secure_filename(f"product_{int(time.time())}_{image_file.filename}")
#                     upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'products')
#                     os.makedirs(upload_folder, exist_ok=True)
#                     filepath = os.path.join(upload_folder, filename)
#                     image_file.save(filepath)
#                     current_images.append(f"/static/uploads/products/{filename}")
            
#             product.image_urls = json.dumps(current_images)
        
#         db.session.commit()
#         return jsonify({'message': 'Product updated successfully'})
        
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error updating product: {str(e)}")
#         return jsonify({'message': 'Failed to update product'}), 500

# @modify_data_bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
# def delete_product(product_id):
#     try:
#         product = Product.query.get_or_404(product_id)
#         db.session.delete(product)
#         db.session.commit()
#         return jsonify({'message': 'Product deleted successfully'})
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error deleting product: {str(e)}")
#         return jsonify({'message': 'Failed to delete product'}), 500

# @modify_data_bp.route('/remove_product_image/<int:product_id>', methods=['POST'])
# def remove_product_image(product_id):
#     try:
#         data = request.json
#         if not data or 'image_url' not in data:
#             return jsonify({'message': 'Image URL is required'}), 400
            
#         product = Product.query.get_or_404(product_id)
#         current_images = json.loads(product.image_urls) if product.image_urls else []
        
#         # Remove the image from the list
#         updated_images = [img for img in current_images if img != data['image_url']]
#         product.image_urls = json.dumps(updated_images)
        
#         # Optional: Delete the actual image file
#         try:
#             if data['image_url'].startswith('/static/uploads/products/'):
#                 image_path = os.path.join(current_app.root_path, data['image_url'][1:])
#                 if os.path.exists(image_path):
#                     os.remove(image_path)
#         except Exception as e:
#             current_app.logger.error(f"Error deleting image file: {str(e)}")
        
#         db.session.commit()
#         return jsonify({'message': 'Image removed successfully'})
        
#     except Exception as e:
#         db.session.rollback()
#         current_app.logger.error(f"Error removing product image: {str(e)}")
#         return jsonify({'message': 'Failed to remove image'}), 500