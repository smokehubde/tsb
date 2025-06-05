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
    monkeypatch.setenv('ENABLE_TOR', '0')
    monkeypatch.setenv('TOR_CONTROL_HOST', 'localhost')
    monkeypatch.setenv('TOR_CONTROL_PORT', '9051')
    monkeypatch.setenv('TOR_CONTROL_PASS', 'passw')

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
    resp = client.post('/tor', data={'enabled': 'on', 'host': '127.0.0.1', 'port': '9052', 'password': 'secret'})
    assert b'Settings updated' in resp.data
    assert os.environ['ENABLE_TOR'] == '1'
    assert os.environ['TOR_CONTROL_HOST'] == '127.0.0.1'
    assert os.environ['TOR_CONTROL_PORT'] == '9052'
    assert os.environ['TOR_CONTROL_PASS'] == 'secret'
    saved = env_file.read_text()
    assert 'ENABLE_TOR=1' in saved
    assert 'TOR_CONTROL_HOST=127.0.0.1' in saved
    assert 'TOR_CONTROL_PORT=9052' in saved
    assert 'TOR_CONTROL_PASS=secret' in saved

def test_check_tor_status_no_controller(monkeypatch):
    import tor_service
    monkeypatch.setattr(tor_service, "Controller", None)
    assert tor_service.check_tor_status() is False
