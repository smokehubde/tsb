from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask

DATABASE_URL = "sqlite:///db.sqlite3"

db = SQLAlchemy()
SessionLocal = sessionmaker()


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    description = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer, unique=True)
    language = db.Column(db.String(10))


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SECRET_KEY'] = 'change-me'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        SessionLocal.configure(bind=db.engine)
    return app
