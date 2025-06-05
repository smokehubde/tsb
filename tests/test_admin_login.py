import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_admin_login(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.sqlite3'
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

    resp = client.post('/login', data={'username': 'admin', 'password': 'pass'})
    assert resp.status_code == 302
    assert resp.headers['Location'].endswith('/')
    with client.session_transaction() as sess:
        assert sess.get('logged_in') is True
