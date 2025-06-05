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
    def __init__(self):
        self.cleared = False

    async def clear(self):
        self.cleared = True


async def call_handler(handler, message, state):
    await handler(message, state)


def test_set_country_shows_shipping(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    monkeypatch.setenv("ENV_FILE", str(env_file))
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path}/test.sqlite3")
    monkeypatch.setenv("BOT_TOKEN", "123456:TEST")
    monkeypatch.setenv("SECRET_KEY", "test")

    if "db" in sys.modules:
        importlib.reload(sys.modules["db"])
    else:
        importlib.import_module("db")
    import db
    app = db.create_app()
    with app.app_context():
        db.db.create_all()
        db.db.session.add(db.ShippingCost(country="DE", cost=4.5))
        db.db.session.commit()

    if "bot" in sys.modules:
        importlib.reload(sys.modules["bot"])
    else:
        importlib.import_module("bot")
    import bot

    msg = DummyMessage("DE")
    state = DummyState()
    asyncio.run(call_handler(bot.set_country, msg, state))

    assert state.cleared is True
    assert any("4.5" in r for r in msg.responses)
    with db.SessionLocal() as session:
        user = session.query(db.User).filter_by(telegram_id=1).first()
        assert user.country == "DE"
