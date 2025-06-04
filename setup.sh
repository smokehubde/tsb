#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install aiogram flask flask_sqlalchemy python-dotenv

if command -v systemctl >/dev/null 2>&1; then
  echo "[Unit]" > bot.service
  cat >> bot.service <<SERVICE
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
ExecStart=$VENV_DIR/bin/python $REPO_DIR/bot.py
Restart=always
[Install]
WantedBy=multi-user.target
SERVICE

  echo "[Unit]" > gui.service
  cat >> gui.service <<SERVICE
Description=Flask Admin GUI
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
ExecStart=$VENV_DIR/bin/python $REPO_DIR/admin_app.py
Restart=always
[Install]
WantedBy=multi-user.target
SERVICE

  systemctl --user daemon-reload
  systemctl --user enable --now bot.service gui.service
  echo "Services installed via systemd."
else
  echo "Run the applications manually via:" >&2
  echo "$VENV_DIR/bin/python bot.py" >&2
  echo "$VENV_DIR/bin/python admin_app.py" >&2
fi

echo "Telegram Bot setup completed."
