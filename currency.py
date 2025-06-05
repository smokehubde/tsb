import requests
from datetime import datetime, timedelta


API_URL = "https://api.exchangerate.host/convert"

# cache exchange rates for a short time to avoid repeated requests
_RATE_CACHE: dict[tuple[str, str], tuple[float, datetime]] = {}
_CACHE_TTL = timedelta(hours=1)

COUNTRY_CURRENCY = {
    "Germany": "EUR",
    "Turkey": "TRY",
    "Russia": "RUB",
    "Poland": "PLN",
}

def _get_rate(from_currency: str, to_currency: str) -> float:
    key = (from_currency, to_currency)
    cached = _RATE_CACHE.get(key)
    if cached and datetime.utcnow() - cached[1] < _CACHE_TTL:
        return cached[0]
    resp = requests.get(API_URL, params={"from": from_currency, "to": to_currency}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rate = data.get("info", {}).get("rate")
    if rate is None:
        raise RuntimeError("no rate returned")
    _RATE_CACHE[key] = (rate, datetime.utcnow())
    return rate


def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert *amount* from one currency to another using exchangerate.host."""
    if from_currency == to_currency:
        return amount
    rate = _get_rate(from_currency, to_currency)
    return amount * rate
