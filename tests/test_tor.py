import importlib
import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_tor_settings(tmp_path, monkeypatch):
    env_file = tmp_path / '.env'
    monkeypatch.setenv('ENV_FILE', str(env_file))
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{tmp_path}/test.sqlite3')
    monkeypatch.setenv('SECRET_KEY', 'test')
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS', 'pass')
    monkeypatch.setenv('TOR_HOST', 'localhost')
    monkeypatch.setenv('TOR_PORT', '9050')

    if 'db' in importlib.sys.modules:
        importlib.reload(importlib.import_module('db'))
    if 'admin_app' in importlib.sys.modules:
        importlib.reload(importlib.import_module('admin_app'))
    admin_app = importlib.import_module('admin_app')
    app = admin_app.app
    client = app.test_client()

    # login
    client.post('/login', data={'username': 'admin', 'password': 'pass'})

    # initial page shows host
    resp = client.get('/tor')
    assert resp.status_code == 200
    assert b'localhost' in resp.data

    # update settings
    resp = client.post('/tor', data={'host': '127.0.0.1', 'port': '9051'})
    assert b'Settings updated' in resp.data
    assert os.environ['TOR_HOST'] == '127.0.0.1'
    assert os.environ['TOR_PORT'] == '9051'
    saved = env_file.read_text()
    assert 'TOR_HOST=127.0.0.1' in saved
    assert 'TOR_PORT=9051' in saved
