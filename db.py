import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask import Flask

# Allow overriding the database via environment variable.
# Falls back to the local SQLite file if not provided.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

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


def get_secret_key():
    """Return the Flask secret key.

    The function first checks the ``SECRET_KEY`` environment variable. If it is
    not set, it tries to read the value from the ``.env`` file whose location is
    defined by the ``ENV_FILE`` environment variable (falling back to
    ``./.env``). When the key is still missing a new random key is generated and
    appended to the ``.env`` file so subsequent runs use the same value.
    """

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
        # If the file cannot be written we still return the generated key
        pass
    return key


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SECRET_KEY'] = get_secret_key()
    db.init_app(app)
    with app.app_context():
        db.create_all()
        SessionLocal.configure(bind=db.engine)
    return app
