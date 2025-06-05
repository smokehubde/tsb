#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"
ENV_FILE="$REPO_DIR/.env"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
# install dependencies defined in requirements.txt to stay in sync with setup.py
pip install -r "$REPO_DIR/requirements.txt"

# load existing variables from .env if present
if [ -f "$ENV_FILE" ]; then
    set -a
    . "$ENV_FILE"
    set +a
else
    touch "$ENV_FILE"
fi

write_env() {
    local name="$1" value="$2"
    if grep -q "^${name}=" "$ENV_FILE"; then
        sed -i "s/^${name}=.*/${name}=${value}/" "$ENV_FILE"
    else
        echo "${name}=${value}" >> "$ENV_FILE"
    fi
}

prompt_var() {
    local name="$1" prompt="$2"
    local value="${!name}"
    if [ -z "$value" ]; then
        read -p "$prompt: " value
    fi
    export "$name"="$value"
    write_env "$name" "$value"
}

prompt_var BOT_TOKEN "BOT_TOKEN"
prompt_var ADMIN_USER "Admin username"
prompt_var ADMIN_PASS "Admin password"
prompt_var SECRET_KEY "Flask SECRET_KEY"

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

if systemctl --user --version >/dev/null 2>&1; then
    systemctl --user daemon-reload
    systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
else
    echo "systemd not available, skipping service creation."
    echo "Start the services manually:" >&2
    echo "  $VENV_DIR/bin/python $REPO_DIR/bot.py" >&2
    echo "  $VENV_DIR/bin/python $REPO_DIR/admin_app.py" >&2
fi

echo "Telegram Bot started. Configure it via Telegram."
echo "Admin GUI available at http://localhost:8000" 
