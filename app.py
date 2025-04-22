import os
from flask import Flask
from flask_migrate import Migrate
from config import Config
from models.models import db
from routes.category import category_bp
from routes.products import product_bp
from routes.admin import admin_bp
from routes.modify import modify_data_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = "sahil"
    app.config.from_object(Config)

    # Set Upload Folder
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "static/uploads")
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(modify_data_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

