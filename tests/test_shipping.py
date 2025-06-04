import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_shipping_admin(tmp_path, monkeypatch):
    env_file = tmp_path / '.env'
    monkeypatch.setenv('ENV_FILE', str(env_file))
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{tmp_path}/test.sqlite3')
    monkeypatch.setenv('SECRET_KEY', 'test')
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS', 'pass')

    if 'db' in importlib.sys.modules:
        importlib.reload(importlib.import_module('db'))
    if 'admin_app' in importlib.sys.modules:
        importlib.reload(importlib.import_module('admin_app'))
    admin_app = importlib.import_module('admin_app')
    app = admin_app.app
    client = app.test_client()

    client.post('/login', data={'username': 'admin', 'password': 'pass'})

    resp = client.post('/shipping', data={'country': 'DE', 'cost': '5.0'})
    assert resp.status_code == 200

    from db import ShippingCost
    with app.app_context():
        entry = ShippingCost.query.filter_by(country='DE').first()
        assert entry is not None
        assert entry.cost == 5.0
