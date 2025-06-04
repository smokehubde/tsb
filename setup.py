import os
import sys
import subprocess
from pathlib import Path
from venv import EnvBuilder

REPO_DIR = Path(__file__).resolve().parent
VENV_DIR = REPO_DIR / "venv"


def create_venv():
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


def install_deps(pip_exe):
    subprocess.check_call([str(pip_exe), "install", "--upgrade", "pip"])
    subprocess.check_call([str(pip_exe), "install", "-r", str(REPO_DIR / "requirements.txt")])


def prompt_env(var):
    value = os.getenv(var)
    if not value:
        value = input(f"{var}: ")
    return value


def create_services(python_exe, env):
    # Only Linux systemd services
    if not sys.platform.startswith("linux"):
        print("Systemd services are only created on Linux. Start the scripts manually:")
        print(f"  {python_exe} bot.py")
        print(f"  {python_exe} admin_app.py")
        return

    bot_service = (REPO_DIR / "bot.service").write_text(f"""[Unit]
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory={REPO_DIR}
Environment=BOT_TOKEN={env['BOT_TOKEN']}
ExecStart={python_exe} {REPO_DIR / 'bot.py'}
Restart=always
[Install]
WantedBy=multi-user.target
""")

    gui_service = (REPO_DIR / "gui.service").write_text(f"""[Unit]
Description=Flask Admin GUI
After=network.target
[Service]
WorkingDirectory={REPO_DIR}
Environment=ADMIN_USER={env['ADMIN_USER']}
Environment=ADMIN_PASS={env['ADMIN_PASS']}
Environment=SECRET_KEY={env['SECRET_KEY']}
ExecStart={python_exe} {REPO_DIR / 'admin_app.py'}
Restart=always
[Install]
WantedBy=multi-user.target
""")

    subprocess.check_call(["systemctl", "--user", "daemon-reload"])
    subprocess.check_call(["systemctl", "--user", "enable", "--now", "bot.service", "gui.service"])


def main():
    python_exe, pip_exe = create_venv()
    install_deps(pip_exe)

    env = {
        var: prompt_env(var)
        for var in ["BOT_TOKEN", "ADMIN_USER", "ADMIN_PASS", "SECRET_KEY"]
    }

    create_services(python_exe, env)
    print("Setup complete.")
    print("Admin GUI available at http://localhost:8000")


if __name__ == "__main__":
    main()
