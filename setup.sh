#!/bin/bash
# Setup script for the Telegram Shop Bot
set -euo pipefail

CREATE_SERVICES=1
for arg in "$@"; do
    case "$arg" in
        --no-services)
            CREATE_SERVICES=0
            ;;
        *)
            echo "Usage: $0 [--no-services]" >&2
            exit 1
            ;;
    esac
done

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$REPO_DIR/venv"
ENV_FILE="$REPO_DIR/.env"

command -v python3 >/dev/null 2>&1 || { echo "python3 not found" >&2; exit 1; }

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"

command -v pip >/dev/null 2>&1 || { echo "pip not found" >&2; exit 1; }

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
    local name="$1" prompt="$2" default="${3:-}"
    local value="${!name:-}"
    if [ -z "$value" ]; then
        if [ -n "$default" ]; then
            read -p "$prompt [$default]: " value
            value="${value:-$default}"
        else
            read -p "$prompt: " value
        fi
    fi
    export "$name"="$value"
    write_env "$name" "$value"
}

prompt_var BOT_TOKEN "BOT_TOKEN"
prompt_var ADMIN_USER "Admin username"

prompt_var ADMIN_PASS "Admin password"
HASHED=$(python3 - <<'EOF'
import bcrypt, os
print(bcrypt.hashpw(os.environ['ADMIN_PASS'].encode(), bcrypt.gensalt()).decode())
EOF
)
write_env ADMIN_PASS_HASH "$HASHED"
unset ADMIN_PASS

prompt_var SECRET_KEY "Flask SECRET_KEY"
prompt_var DATABASE_URL "Database URL" "sqlite:///db.sqlite3"
prompt_var ADMIN_HOST "Admin host" "127.0.0.1"
prompt_var ADMIN_PORT "Admin port" "8000"
prompt_var WEBHOOK_URL "Webhook URL (leave empty for polling)"
prompt_var WEBHOOK_HOST "Webhook host" "0.0.0.0"
prompt_var WEBHOOK_PORT "Webhook port" "8080"
prompt_var WEBHOOK_PATH "Webhook path" "/webhook"
prompt_var ENABLE_TOR "Enable Tor (1/0)" "0"
prompt_var TOR_CONTROL_HOST "Tor control host" "127.0.0.1"
prompt_var TOR_CONTROL_PORT "Tor control port" "9051"
prompt_var TOR_CONTROL_PASS "Tor control password"

# file containing the onion URL if Tor is enabled
ONION_FILE="$REPO_DIR/onion_url.txt"
write_env ONION_FILE "$ONION_FILE"

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

if [ "$CREATE_SERVICES" -eq 1 ]; then
    if systemctl --user --version >/dev/null 2>&1; then
        systemctl --user daemon-reload
        systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
    else
        echo "systemd not available, skipping service creation."
        echo "Start the services manually:" >&2
        echo "  $VENV_DIR/bin/python $REPO_DIR/bot.py" >&2
        echo "  $VENV_DIR/bin/python $REPO_DIR/admin_app.py" >&2
    fi
else
    echo "Skipping service creation (--no-services)."
fi

echo "Telegram Bot started. Configure it via Telegram."

echo "Admin GUI available at http://localhost:8000"

# wait for Tor hidden service information if available
if [ "$ENABLE_TOR" = "1" ] && [ -n "$ONION_FILE" ]; then
    echo -n "Waiting for Tor address..."
    for _ in {1..10}; do
        if [ -f "$ONION_FILE" ]; then
            echo
            echo "Admin GUI via Tor: $(cat "$ONION_FILE")"
            break
        fi
        sleep 1
        echo -n "."
    done
    if [ ! -f "$ONION_FILE" ]; then
        echo
        echo "Tor onion address not found. Check admin.log for details." >&2
    fi
fi

echo "Admin GUI available at http://${ADMIN_HOST:-localhost}:${ADMIN_PORT:-8000}"

