from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)  # New field for category image
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    # Store specifications as JSON
    specs = db.Column(db.JSON, nullable=True)  # ✅ Dynamic product features

    # Store image and video URLs as JSON
    image_urls = db.Column(db.JSON, nullable=True)  # ✅ Store image URLs in a list
    video_url = db.Column(db.String(255), nullable=True)  # ✅ Store video link
    
    def __repr__(self):
        return f"<Product {self.name}>"