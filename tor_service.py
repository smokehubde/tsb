# -*- coding: utf-8 -*-
"""Utilities to work with Tor hidden services."""

from __future__ import annotations

import os
from contextlib import contextmanager
from typing import Generator

try:
    from stem.control import Controller
except ImportError:  # pragma: no cover - optional dependency
    Controller = None


def _get_tor_config() -> tuple[str, int, str | None, int]:
    host = os.getenv("TOR_CONTROL_HOST", "127.0.0.1")
    port = int(os.getenv("TOR_CONTROL_PORT", "9051"))
    password = os.getenv("TOR_CONTROL_PASS")
    service_port = int(os.getenv("TOR_SERVICE_PORT", "80"))
    return host, port, password, service_port


@contextmanager
def hidden_service(local_port: int) -> Generator[str, None, None]:
    """Create an ephemeral Tor hidden service mapping ``local_port``."""
    host, port, password, service_port = _get_tor_config()
    if Controller is None:
        raise RuntimeError("stem is required to use the hidden service feature")

    controller = Controller.from_port(address=host, port=port)
    controller.authenticate(password=password)
    hs = controller.create_ephemeral_hidden_service({service_port: local_port}, await_publication=True)
    onion = f"{hs.service_id}.onion"
    try:
        yield onion
    finally:
        controller.remove_ephemeral_hidden_service(hs.service_id)
        controller.close()


def check_tor_status() -> bool:
    """Return ``True`` if a connection to the Tor control port succeeds."""
    if Controller is None:
        return False
    host, port, password, _ = _get_tor_config()
    try:
        with Controller.from_port(address=host, port=port) as ctrl:
            ctrl.authenticate(password=password)
            return True
    except Exception:
        return False
