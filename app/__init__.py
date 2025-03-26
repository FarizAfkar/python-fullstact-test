from flask import Flask
from app.config import Config
from app.db import init_db
from app.routes import client_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    init_db()

    # Register routes
    app.register_blueprint(client_bp)

    return app