from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # (No SQLAlchemy initialisation needed now because we use psycopg2 directly.)

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)
    
    return app
