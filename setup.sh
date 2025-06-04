#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"
ENV_FILE="$REPO_DIR/tsb.env"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install aiogram flask flask_sqlalchemy

if [ ! -f "$ENV_FILE" ]; then
  cat > "$ENV_FILE" <<EOF
BOT_TOKEN=
ADMIN_USER=admin
ADMIN_PASS=q12wq12w
EOF
  echo "Created example environment file at $ENV_FILE"
fi

if [[ "$(uname -s)" == "Linux" && -n "$(command -v systemctl)" ]]; then
  echo "[Unit]" > bot.service
  cat >> bot.service <<SERVICE
Description=Telegram Shop Bot
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$VENV_DIR/bin/python $REPO_DIR/bot.py
Restart=always
[Install]
WantedBy=default.target
SERVICE

  echo "[Unit]" > gui.service
  cat >> gui.service <<SERVICE
Description=Flask Admin GUI
After=network.target
[Service]
WorkingDirectory=$REPO_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$VENV_DIR/bin/python $REPO_DIR/admin_app.py
Restart=always
[Install]
WantedBy=default.target
SERVICE

  systemctl --user daemon-reload
  systemctl --user enable --now bot.service gui.service
  echo "Services installed. Admin GUI available at http://localhost:8000"
else
  echo "Systemd not available. Start the applications manually with:" >&2
  echo "source $ENV_FILE && $VENV_DIR/bin/python bot.py" >&2
  echo "source $ENV_FILE && $VENV_DIR/bin/python admin_app.py" >&2
fi

echo "Setup complete."
