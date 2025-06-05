import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_upload_image(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.sqlite3'
    img = tmp_path / 'img.png'
    img.write_bytes(b'fake')
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_path}')
    monkeypatch.setenv('SECRET_KEY', 'test')
    import bcrypt
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS_HASH', bcrypt.hashpw(b'pass', bcrypt.gensalt()).decode())
    monkeypatch.setenv('FLASK_ENV', 'test')

    if 'db' in importlib.sys.modules:
        importlib.reload(importlib.import_module('db'))
    if 'admin_app' in importlib.sys.modules:
        importlib.reload(importlib.import_module('admin_app'))
    admin_app = importlib.import_module('admin_app')
    app = admin_app.app
    client = app.test_client()

    client.post('/login', data={'username': 'admin', 'password': 'pass'})
    data = {
        'name': 'Prod',
        'price': '1.0',
        'description': 'Desc'
    }
    with img.open('rb') as f:
        data['image'] = f
        resp = client.post('/add', data=data, content_type='multipart/form-data')
    assert resp.status_code == 302

    with app.app_context():
        from db import Product
        p = Product.query.first()
        assert p.image_path
