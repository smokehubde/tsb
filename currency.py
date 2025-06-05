import requests

API_URL = "https://api.exchangerate.host/convert"

COUNTRY_CURRENCY = {
    "Germany": "EUR",
    "Turkey": "TRY",
    "Russia": "RUB",
    "Poland": "PLN",
}

def convert(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert *amount* from one currency to another using exchangerate.host."""
    if from_currency == to_currency:
        return amount
    resp = requests.get(API_URL, params={"from": from_currency, "to": to_currency}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rate = data.get("info", {}).get("rate")
    if rate is None:
        raise RuntimeError("no rate returned")
    return amount * rate
