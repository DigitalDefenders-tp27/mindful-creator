# backend/app/__init__.py
import os
from flask import Flask
from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__)

    # ── CORS ────────────────────────────────────────────────────────────────
    #
    # 1. read the origin from .env  (CORS_ORIGIN=http://localhost:5173)
    # 2. allow automatic OPTIONS handling
    # 3. during local dev we don’t need credentials cookies → supports_credentials=False
    #
    cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173")
    CORS(
        app,
        resources={r"/api/*": {"origins": cors_origin}},
        methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
        max_age=3600,          # cache pre‑flight for 1 hour
    )

    # ── Blueprints ──────────────────────────────────────────────────────────
    from .routes import main
    app.register_blueprint(main)

    return app
