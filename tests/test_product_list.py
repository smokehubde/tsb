import asyncio
import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))


class DummyUser:
    def __init__(self, user_id):
        self.id = user_id


class DummyMessage:
    def __init__(self, text, user_id=1):
        self.text = text
        self.from_user = DummyUser(user_id)
        self.responses = []

    async def answer(self, text, reply_markup=None):
        self.responses.append(text)


class DummyState:
    async def set_state(self, state):
        self.state = state

async def call_handler(handler, message, state):
    await handler(message, state)


def test_cmd_start_lists_products(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    monkeypatch.setenv("ENV_FILE", str(env_file))
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.sqlite3")
    monkeypatch.setenv("BOT_TOKEN", "123:TEST")
    monkeypatch.setenv("SECRET_KEY", "test")

    if "models" in sys.modules:
        importlib.reload(sys.modules["models"])
    else:
        importlib.import_module("models")
    if "database" in sys.modules:
        importlib.reload(sys.modules["database"])
    else:
        importlib.import_module("database")
    import models as db
    import database
    app = database.create_app()
    with app.app_context():
        db.db.create_all()
        db.db.session.add(db.User(telegram_id=1, language="de", country="DE"))
        db.db.session.add(db.Product(name="Prod1", price=1.0, description="Desc"))
        db.db.session.commit()

    if "bot" in sys.modules:
        importlib.reload(sys.modules["bot"])
    else:
        importlib.import_module("bot")
    import bot

    msg = DummyMessage("/start")
    state = DummyState()
    asyncio.run(call_handler(bot.cmd_start, msg, state))

    assert any("Prod1" in r for r in msg.responses)
