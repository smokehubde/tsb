# -*- coding: utf-8 -*-
"""Environment setup helper for the Telegram Shop Bot."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from venv import EnvBuilder

REPO_DIR = Path(__file__).resolve().parent
VENV_DIR = REPO_DIR / "venv"
ENV_FILE = REPO_DIR / ".env"


def create_venv() -> tuple[Path, Path]:
    if not VENV_DIR.exists():
        builder = EnvBuilder(with_pip=True)
        builder.create(VENV_DIR)
    if sys.platform == "win32":
        python_exe = VENV_DIR / "Scripts" / "python.exe"
        pip_exe = VENV_DIR / "Scripts" / "pip.exe"
    else:
        python_exe = VENV_DIR / "bin" / "python"
        pip_exe = VENV_DIR / "bin" / "pip"
    return python_exe, pip_exe


def install_deps(pip_exe: Path) -> None:
    subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])
    subprocess.check_call([str(pip_exe), "install", "-r", str(REPO_DIR / "requirements.txt")])


def prompt_env(var: str) -> str:
    value = os.getenv(var)
    if not value:
        value = input(f"{var}: ")
    os.environ[var] = value
    return value


def load_env_file() -> dict[str, str]:
    data: dict[str, str] = {}
    if ENV_FILE.exists():
        with ENV_FILE.open() as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    data[k] = v
    return data


def write_env_file(env: dict[str, str]) -> None:
    with ENV_FILE.open("w") as f:
        for k, v in env.items():
            f.write(f"{k}={v}\n")


def create_services(python_exe: Path, env: dict[str, str]) -> None:
    if not sys.platform.startswith("linux"):
        print("Systemd services are only created on Linux. Start the scripts manually:")
        print(f"  {python_exe} bot.py")
        print(f"  {python_exe} admin_app.py")
        return

    try:
        subprocess.check_call(["systemctl", "--user", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        (REPO_DIR / "bot.service").write_text(
            f"""[Unit]
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory={REPO_DIR}
EnvironmentFile={ENV_FILE}
ExecStart={python_exe} {REPO_DIR / 'bot.py'}
Restart=always
[Install]
WantedBy=default.target
"""
        )

        (REPO_DIR / "gui.service").write_text(
            f"""[Unit]
Description=Flask Admin GUI
After=network.target
[Service]
WorkingDirectory={REPO_DIR}
EnvironmentFile={ENV_FILE}
ExecStart={python_exe} {REPO_DIR / 'admin_app.py'}
Restart=always
[Install]
WantedBy=default.target
"""
        )

        subprocess.check_call(["systemctl", "--user", "daemon-reload"])
        subprocess.check_call([
            "systemctl",
            "--user",
            "enable",
            "--now",
            str(REPO_DIR / "bot.service"),
            str(REPO_DIR / "gui.service"),
        ])
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("systemd not available or command failed. Start the scripts manually:")
        print(f"  {python_exe} bot.py")
        print(f"  {python_exe} admin_app.py")
        return


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-services", action="store_true", help="skip systemd service creation")
    args = parser.parse_args(argv)

    python_exe, pip_exe = create_venv()
    install_deps(pip_exe)

    import bcrypt

    env = load_env_file()
    for var in ["BOT_TOKEN", "ADMIN_USER", "SECRET_KEY"]:
        env[var] = env.get(var) or prompt_env(var)
    password = env.get("ADMIN_PASS") or prompt_env("ADMIN_PASS")
    env["ADMIN_PASS_HASH"] = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    env.pop("ADMIN_PASS", None)

    write_env_file(env)

    if not args.no_services:
        create_services(python_exe, env)
    print("Setup complete.")
    print("Admin GUI available at http://localhost:8000")


if __name__ == "__main__":
    main()
