import os
import importlib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_bot_token_from_env_file(tmp_path, monkeypatch):
    env = tmp_path / '.env'
    env.write_text('BOT_TOKEN=123456:ABC\n')
    monkeypatch.setenv('ENV_FILE', str(env))
    if 'bot' in importlib.sys.modules:
        importlib.reload(importlib.import_module('bot'))
    import bot
    assert bot.get_bot_token() == '123456:ABC'
