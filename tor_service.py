import os
from stem.control import Controller

class TorService:
    def __init__(self):
        self.enable = os.getenv("ENABLE_TOR") == "1"
        self.host = os.getenv("TOR_CONTROL_HOST", "127.0.0.1")
        self.port = int(os.getenv("TOR_CONTROL_PORT", "9051"))
        self.password = os.getenv("TOR_CONTROL_PASS")
        self.service_id = None
        self.onion = None

    def setup(self, local_port: int):
        if not self.enable:
            return None
        with Controller.from_port(address=self.host, port=self.port) as c:
            if self.password:
                c.authenticate(password=self.password)
            else:
                c.authenticate()
            res = c.create_ephemeral_hidden_service({80: local_port}, await_publication=True)
            self.service_id = res.service_id
            self.onion = f"{res.service_id}.onion"
            return self.onion

    def remove(self):
        if not self.enable or not self.service_id:
            return
        with Controller.from_port(address=self.host, port=self.port) as c:
            if self.password:
                c.authenticate(password=self.password)
            else:
                c.authenticate()
            c.remove_ephemeral_hidden_service(self.service_id)
        self.service_id = None
        self.onion = None

    def regenerate(self, local_port: int):
        self.remove()
        return self.setup(local_port)
