# Telegram Shop Bot

Dieses Projekt beinhaltet einen einfachen Telegram-Bot und eine Admin-Oberfl\xe4che zum Verwalten von Produkten. The bot uses aiogram 3.x and the admin GUI is built with Flask.

## Features / Funktionen

* Bot asks for the language on `/start` (Deutsch oder Englisch) and stores the setting.
* First menu shows "W\xe4hle ein Produkt" or "Choose a product" accordingly.
* Admin login using the credentials from `ADMIN_USER` and `ADMIN_PASS`.
* Manage products with name, price and description.
* Manage shipping costs per country.
* After selecting the country the bot shows the shipping fee.
* The GUI runs locally on port 8000.
* New `/tor` route allows controlling Tor using the environment variables `ENABLE_TOR`, `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` and `TOR_CONTROL_PASS`.

## Setup / Einrichtung

Python 3 is required (on some systems the command is `python3`).

### Schritt-f\xfcr-Schritt / Step-by-step

1. **Repository klonen / Clone the repository**
   ```bash
   git clone https://example.com/tsb.git
   cd tsb
   ```
2. **Setup-Skript ausf\xfchren / Run the setup script** – choose the Bash or Python version depending on your platform. The script creates a virtual environment, installs all dependencies and prompts for:
   - `BOT_TOKEN` – Telegram bot token
   - `ADMIN_USER` – admin username
   - `ADMIN_PASS_HASH` – hashed admin password
   - `SECRET_KEY` – secret key for Flask
   - optional settings like database URL or webhook parameters
   ```bash
   ./setup.sh [--no-services]  # Linux/macOS
   # or
   python3 setup.py  # Windows or alternative
   ```
   The answers are stored in `.env` and can be modified later.
3. **Dienste starten / Start the services** – on Linux the scripts configure and start systemd units. On other systems run bot and GUI manually:
   ```bash
   python3 bot.py
   python3 admin_app.py
   ```
   If you skipped the setup script install the requirements manually:
   ```bash
   pip install -r requirements.txt
   ```
   The scripts create a virtual environment under `venv`, install the dependencies and write your values to `.env`. On Linux, systemd units are enabled immediately using:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
   ```
   If `systemctl --user` is not available, start bot and GUI manually:
   ```bash
   python3 bot.py
   python3 admin_app.py
   ```

After starting, the bot is reachable via Telegram (set the token with `BOT_TOKEN`) and the admin GUI is available at [http://localhost:8000](http://localhost:8000). Log files `bot.log` and `admin.log` are created in the directory configured as `WorkingDirectory`. The setup script also prints a Tor address stored in `onion_url.txt`. Make sure the `tor` service is running with a reachable control port (default `9051`) or the message `Tor onion address not found` will appear.

### So pr\xfcfst du dein Setup / Verify your setup

```bash
pytest
```

## Umgebungsvariablen / Environment Variables

Die systemd-Dienste laden ihre Konfiguration aus der Datei `.env`. Eine Beispieldatei `.env.example` liegt bei und enth\xe4lt folgende Variablen:

* `BOT_TOKEN` – Telegram token for the bot
* `ADMIN_USER` – username for the admin login
* `ADMIN_PASS_HASH` – hashed password for the admin login
* `SECRET_KEY` – Flask `SECRET_KEY` for the web interface
* `DATABASE_URL` – optional database URL (default: `sqlite:///db.sqlite3`)
* `ADMIN_HOST` – hostname/IP for the admin GUI (default: `127.0.0.1`)
* `ADMIN_PORT` – port of the admin GUI (default: `8000`)
* `WEBHOOK_URL` – HTTPS URL for Telegram webhooks (optional)
* `WEBHOOK_HOST` – hostname/IP for the webhook server (default: `0.0.0.0`)
* `WEBHOOK_PORT` – port for the webhook server (default: `8080`)
* `WEBHOOK_PATH` – path for the webhook route (default: `/webhook`)
* `ENABLE_TOR` – set to `1` to expose the admin GUI via Tor
* `TOR_CONTROL_HOST` – host of the Tor control port (default: `127.0.0.1`)
* `TOR_CONTROL_PORT` – port of the Tor control port (default: `9051`)
* `TOR_CONTROL_PASS` – password for the Tor control port
* `ONION_FILE` – file where the generated Tor URL is stored (default: `onion_url.txt`)

Diese Werte k\xf6nnen in einer `.env`-Datei gespeichert werden. This file must **not** be committed to the repository.

## Tests

Unit tests are executed using pytest. After installing the dependencies you can run them directly with `pytest`.

## Lizenz / License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
