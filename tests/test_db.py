import sys
import importlib
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_create_product(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.sqlite3'
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_path}')
    monkeypatch.setenv('SECRET_KEY', 'test')
    importlib.reload(importlib.import_module('db'))
    from db import create_app, SessionLocal, Product
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
