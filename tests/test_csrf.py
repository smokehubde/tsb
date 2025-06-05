import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_csrf_error_returns_400(tmp_path, monkeypatch):
    db_path = tmp_path / "test.sqlite3"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("SECRET_KEY", "test")
    import bcrypt
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASS_HASH", bcrypt.hashpw(b"pass", bcrypt.gensalt()).decode())
    # ensure production mode
    monkeypatch.delenv("FLASK_ENV", raising=False)

    if "db" in sys.modules:
        importlib.reload(sys.modules["db"])
    if "admin_app" in sys.modules:
        importlib.reload(sys.modules["admin_app"])
    admin_app = importlib.import_module("admin_app")
    app = admin_app.app
    client = app.test_client()

    resp = client.post("/login", data={"username": "admin", "password": "pass"})
    assert resp.status_code == 400
