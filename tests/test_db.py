import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import importlib


def test_create_product(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.sqlite3'
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_path}')
    monkeypatch.setenv('SECRET_KEY', 'test')
    importlib.reload(importlib.import_module('models'))
    importlib.reload(importlib.import_module('database'))
    from database import create_app
    from models import SessionLocal, Product
    app = create_app()
    with app.app_context():
        with SessionLocal() as session:
            product = Product(name='Test', price=9.99, description='demo')
            session.add(product)
            session.commit()
            assert session.query(Product).count() == 1
            stored = session.query(Product).first()
            assert stored.name == 'Test'
            assert stored.price == 9.99
            assert stored.description == 'demo'
