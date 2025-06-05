from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Global database objects used across the application

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
