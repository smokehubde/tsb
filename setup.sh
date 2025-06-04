#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install -r "$REPO_DIR/requirements.txt"

SYSTEMD_USER_DIR="$HOME/.config/systemd/user"
mkdir -p "$SYSTEMD_USER_DIR"

echo "[Unit]" > "$SYSTEMD_USER_DIR/bot.service"
cat >> "$SYSTEMD_USER_DIR/bot.service" <<SERVICE
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
ExecStart=$VENV_DIR/bin/python $REPO_DIR/bot.py
Restart=always
[Install]
WantedBy=multi-user.target
SERVICE


echo "[Unit]" > "$SYSTEMD_USER_DIR/gui.service"
cat >> "$SYSTEMD_USER_DIR/gui.service" <<SERVICE
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

echo "Telegram Bot started. Configure it via Telegram."
echo "Admin GUI available at http://localhost:8000" 
