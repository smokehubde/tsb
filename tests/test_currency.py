import importlib
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_convert_calls_api(monkeypatch):
    from currency import convert

    class DummyResp:
        def __init__(self, json_data):
            self._data = json_data

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    called = {}

    def fake_get(url, params=None, timeout=10):
        called['url'] = url
        called['params'] = params
        return DummyResp({'info': {'rate': 2.0}})

    monkeypatch.setattr('requests.get', fake_get)

    result = convert(3, 'EUR', 'XYZ')
    assert result == 6
    assert called['params']['from'] == 'EUR'
    assert called['params']['to'] == 'XYZ'
