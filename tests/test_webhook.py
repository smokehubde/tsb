import importlib
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import aiogram
from aiohttp import web


def test_webhook_mode(monkeypatch):
    monkeypatch.setenv('BOT_TOKEN', '123456:TEST')
    monkeypatch.setenv('WEBHOOK_URL', 'https://example.com/hook')
    import bcrypt
    monkeypatch.setenv('SECRET_KEY', 'test')
    monkeypatch.setenv('ADMIN_USER', 'admin')
    monkeypatch.setenv('ADMIN_PASS_HASH', bcrypt.hashpw(b'pass', bcrypt.gensalt()).decode())
    monkeypatch.setenv('FLASK_ENV', 'test')

    calls = {}

    async def fake_set_webhook(self, url):
        calls['set'] = url

    async def fake_delete_webhook(self):
        calls['delete'] = True

    def fake_run_app(app, host=None, port=None, loop=None):
        calls['run'] = (host, port)
        for cb in app.on_startup:
            loop.run_until_complete(cb(app))
        for cb in app.on_shutdown:
            loop.run_until_complete(cb(app))

    monkeypatch.setattr(aiogram.Bot, 'set_webhook', fake_set_webhook)
    monkeypatch.setattr(aiogram.Bot, 'delete_webhook', fake_delete_webhook)
    monkeypatch.setattr(web, 'run_app', fake_run_app)

    if 'bot' in sys.modules:
        importlib.reload(sys.modules['bot'])
    else:
        importlib.import_module('bot')

    import bot
    monkeypatch.setattr(bot, 'create_app', lambda: None)

    bot.main()

    assert calls['set'] == 'https://example.com/hook'
    assert calls['delete'] is True
    assert calls['run'] == ('0.0.0.0', 8080)

