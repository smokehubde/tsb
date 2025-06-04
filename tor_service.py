import os
from contextlib import contextmanager

try:
    from stem.control import Controller
except ImportError:  # pragma: no cover - stem is an optional dependency in tests
    Controller = None


def _get_tor_config():
    control_port = int(os.getenv("TOR_CONTROL_PORT", "9051"))
    password = os.getenv("TOR_PASSWORD")
    service_port = int(os.getenv("TOR_SERVICE_PORT", "80"))
    return control_port, password, service_port


@contextmanager
def hidden_service(local_port):
    """Context manager that creates an ephemeral Tor hidden service."""
    control_port, password, service_port = _get_tor_config()
    if Controller is None:
        raise RuntimeError("stem is required to use the hidden service feature")

    controller = Controller.from_port(port=control_port)
    controller.authenticate(password=password)
    hs = controller.create_ephemeral_hidden_service({service_port: local_port}, await_publication=True)
    onion = f"{hs.service_id}.onion"
    try:
        yield onion
    finally:
        controller.remove_ephemeral_hidden_service(hs.service_id)
        controller.close()
