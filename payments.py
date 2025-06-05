import json
import subprocess
from typing import Optional


def create_wallet(amount: float) -> str:
    """Return a new address for *amount* using Electrum CLI."""
    result = subprocess.check_output(["electrum", "createnewaddress"]).decode().strip()
    return result


def check_payment(address: str, amount: float) -> bool:
    """Return True if *amount* was received on *address*."""
    try:
        output = subprocess.check_output(["electrum", "getreceived", address, "-f", "json"]).decode()
        data = json.loads(output)
        received = float(data.get(address, 0))
        return received >= amount
    except Exception:
        return False
