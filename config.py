"""Configuration utilities for the Telegram Shop Bot."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


def load_env(path: str | None = None) -> None:
    """Load variables from a .env file.

    If *path* is provided or the ``ENV_FILE`` environment variable is set,
    variables from that file override existing ones. Otherwise values are only
    added when missing.
    """
    env_path = path or os.getenv("ENV_FILE", str(Path(__file__).with_name(".env")))
    if not os.path.exists(env_path):
        return

    override = path is not None or "ENV_FILE" in os.environ
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, value = line.strip().split("=", 1)
                if override:
                    os.environ[key] = value
                else:
                    os.environ.setdefault(key, value)


def setup_logging(level: int = logging.INFO, log_file: str = "app.log") -> None:
    """Configure root logging with a rotating file handler."""
    handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[handler, logging.StreamHandler()])
