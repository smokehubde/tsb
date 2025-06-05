import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_shipping_admin(tmp_path, monkeypatch):
    env_file = tmp_path / '.env'
    monkeypatch.setenv('ENV_FILE', str(env_file))
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{tmp_path}/test.sqlite3')
    monkeypatch.setenv('SECRET_KEY', 'test')
    from werkzeug.security import generate_password_hash
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS_HASH', generate_password_hash('pass'))
    monkeypatch.setenv('FLASK_ENV', 'test')

    if 'models' in importlib.sys.modules:
        importlib.reload(importlib.import_module('models'))
    if 'database' in importlib.sys.modules:
        importlib.reload(importlib.import_module('database'))
    if 'admin' in importlib.sys.modules:
        importlib.reload(importlib.import_module('admin'))
    admin_app = importlib.import_module('admin')
    app = admin_app.app
    client = app.test_client()

    client.post('/login', data={'username': 'admin', 'password': 'pass'})

    resp = client.post('/shipping', data={'country': 'DE', 'cost': '5.0'})
    assert resp.status_code == 200

    from models import ShippingCost
    with app.app_context():
        entry = ShippingCost.query.filter_by(country='DE').first()
        assert entry is not None
        assert entry.cost == 5.0
