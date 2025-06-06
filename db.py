# -*- coding: utf-8 -*-
"""Database models and application factory."""

from __future__ import annotations

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Allow overriding the database via environment variable.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")


db = SQLAlchemy()
SessionLocal = sessionmaker()


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.String(255))
    image_path = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    language = db.Column(db.String(10))
    country = db.Column(db.String(50))


class ShippingCost(db.Model):
    __tablename__ = "shipping_costs"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(50), unique=True)
    cost = db.Column(db.Float)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    wallet_address = db.Column(db.String(255))
    amount = db.Column(db.Float)
    paid = db.Column(db.Boolean, default=False)


def get_secret_key() -> str:
    """Return the Flask secret key, creating one if necessary."""
    key = os.getenv("SECRET_KEY")
    if key:
        return key

    env_path = os.getenv("ENV_FILE", os.path.join(os.path.dirname(__file__), ".env"))
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.startswith("SECRET_KEY="):
                    key = line.strip().split("=", 1)[1]
                    os.environ["SECRET_KEY"] = key
                    return key

    import secrets

    key = secrets.token_urlsafe(16)
    os.environ["SECRET_KEY"] = key
    try:
        with open(env_path, "a") as f:
            f.write(f"SECRET_KEY={key}\n")
    except OSError:
        pass
    return key


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SECRET_KEY"] = get_secret_key()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        SessionLocal.configure(bind=db.engine)
    return app
