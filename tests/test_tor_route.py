import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_tor_route(tmp_path, monkeypatch):
    db_path = tmp_path / 'test.sqlite3'
    monkeypatch.setenv('DATABASE_URL', f'sqlite:///{db_path}')
    monkeypatch.setenv('SECRET_KEY', 'test')
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS', 'pass')

    if 'db' in importlib.sys.modules:
        importlib.reload(importlib.import_module('db'))

    dummy_controller = MagicMock()
    dummy_controller.__enter__.return_value = dummy_controller
    dummy_controller.__exit__.return_value = False
    dummy_controller.authenticate.return_value = True

    with patch('stem.control.Controller.from_port', return_value=dummy_controller) as mock_from_port:
        if 'admin_app' in importlib.sys.modules:
            importlib.reload(importlib.import_module('admin_app'))
        admin_app = importlib.import_module('admin_app')
        app = admin_app.app
        client = app.test_client()

        resp = client.get('/tor')
        assert resp.status_code == 200
        assert resp.json == {'status': 'ok'}
        mock_from_port.assert_called_once()
