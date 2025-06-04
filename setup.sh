#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install aiogram flask flask_sqlalchemy

if [ -z "$BOT_TOKEN" ]; then
    read -p "BOT_TOKEN: " BOT_TOKEN
fi
if [ -z "$ADMIN_USER" ]; then
    read -p "Admin username: " ADMIN_USER
fi
if [ -z "$ADMIN_PASS" ]; then
    read -p "Admin password: " ADMIN_PASS
fi
if [ -z "$SECRET_KEY" ]; then
    read -p "Flask SECRET_KEY: " SECRET_KEY
fi

echo "[Unit]" > bot.service
cat >> bot.service <<SERVICE
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
Environment=BOT_TOKEN=$BOT_TOKEN
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
Environment=ADMIN_USER=$ADMIN_USER
Environment=ADMIN_PASS=$ADMIN_PASS
Environment=SECRET_KEY=$SECRET_KEY
ExecStart=$VENV_DIR/bin/python $REPO_DIR/admin_app.py
Restart=always
[Install]
WantedBy=multi-user.target
SERVICE

systemctl --user daemon-reload
systemctl --user enable --now bot.service gui.service

echo "Telegram Bot started. Configure it via Telegram."
echo "Admin GUI available at http://localhost:8000" 
