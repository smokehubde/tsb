import sys
from pathlib import Path
import importlib

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_create_wallet(monkeypatch):
    called = {}
    def fake_check(cmd):
        called['cmd'] = cmd
        return b'addr'
    monkeypatch.setattr('subprocess.check_output', fake_check)
    import payments
    addr = payments.create_wallet(1.0)
    assert addr == 'addr'
    assert called['cmd'][0] == 'electrum'


def test_check_payment(monkeypatch):
    def fake_check(cmd):
        return b'{"addr": 1.0}'
    monkeypatch.setattr('subprocess.check_output', fake_check)
    import payments
    assert payments.check_payment('addr', 1.0)
