from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialise SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

     # PostgreSQL DB configuration from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise the db with the app
    db.init_app(app)
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app
