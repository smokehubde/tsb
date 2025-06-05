# Telegram Shop Bot

Dieses Projekt enthält einen einfachen Telegram-Bot und eine Admin-Oberfläche zum Verwalten von Produkten. The bot uses aiogram 3.x and the admin GUI is built with Flask.

## Funktionen / Features

- Bot fragt bei `/start` nach der Sprache (Deutsch oder Englisch) und speichert die Auswahl / On `/start` the bot asks for the preferred language and remembers it.
- Erste Menü-Ausgabe "Wähle ein Produkt" bzw. "Choose a product" je nach Sprache.
- Admin-Login über `ADMIN_USER` und `ADMIN_PASS`.
- Verwaltung von Produkten mit Name, Preis und Beschreibung / Manage products with name, price and description.
- Versandkosten pro Land verwalten / Manage shipping costs per country.
- Nach Auswahl des Landes zeigt der Bot die Versandkosten an / After selecting the country the bot shows the shipping fee.
- GUI läuft lokal auf Port 8000 / The GUI runs locally on port 8000.
- Neue Route `/tor` ermöglicht das Steuern des Tor-Dienstes über `ENABLE_TOR`, `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` und `TOR_CONTROL_PASS` / `/tor` route controls Tor using those environment variables.

## Setup / Einrichtung

Python 3 wird benötigt (auf manchen Systemen `python3`). / Python 3 is required.

### Schritt für Schritt / Step by step

1. **Repository klonen / Clone the repository**
   ```bash
   git clone https://example.com/tsb.git
   cd tsb
   ```
2. **Setup-Skript ausführen / Run the setup script**
   ```bash
   ./setup.sh [--no-services]  # Linux/macOS
   # or / oder
   python3 setup.py            # Windows
   ```
   Das Skript legt eine virtuelle Umgebung an, installiert alle Abhängigkeiten und fragt Werte wie `BOT_TOKEN`, `ADMIN_USER`, `ADMIN_PASS`, `SECRET_KEY` usw. ab. Die Antworten werden in `.env` gespeichert.
3. **Dienste starten / Start the services**
   ```bash
   python3 bot.py
   python3 admin_app.py
   ```
   Auf Linux richten die Skripte systemd-Dienste ein:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
   ```

Nach dem Start ist der Bot über Telegram erreichbar und die Admin-GUI unter [http://localhost:8000](http://localhost:8000). Die Skripte schreiben Logdateien `bot.log` und `admin.log`. Nach dem Setup wird außerdem eine Datei `onion_url.txt` mit der Tor-Adresse erzeugt, sofern `tor` mit einem erreichbaren ControlPort (Standard `9051`) läuft.

### Tests

```bash
pytest
```

## Umgebungsvariablen / Environment Variables

Die Dienste lesen ihre Konfiguration aus `.env`. The following variables are supported:

* `BOT_TOKEN` – Telegram token for the bot
* `ADMIN_USER` – admin username
* `ADMIN_PASS_HASH` – hashed admin password
* `SECRET_KEY` – Flask secret key
* `DATABASE_URL` – database URL (default `sqlite:///db.sqlite3`)
* `ADMIN_HOST` – host for the admin GUI (default `127.0.0.1`)
* `ADMIN_PORT` – port for the admin GUI (default `8000`)
* `WEBHOOK_URL` – HTTPS URL for Telegram webhooks (optional)
* `WEBHOOK_HOST` – host for the webhook server (default `0.0.0.0`)
* `WEBHOOK_PORT` – port for the webhook server (default `8080`)
* `WEBHOOK_PATH` – path for the webhook route (default `/webhook`)
* `ENABLE_TOR` – set `1` to expose the GUI via Tor
* `TOR_CONTROL_HOST` – Tor control host (default `127.0.0.1`)
* `TOR_CONTROL_PORT` – Tor control port (default `9051`)
* `TOR_CONTROL_PASS` – password for the Tor control port
* `ONION_FILE` – file storing the generated Tor URL (default `onion_url.txt`)

Diese Werte sollten in einer `.env`-Datei gespeichert werden und dürfen nicht ins Repository eingecheckt werden. Wird `ADMIN_HOST` auf `0.0.0.0` gesetzt oder der Tor-Dienst aktiviert, ist die Admin-Oberfläche von außen erreichbar. Verwende ein starkes Passwort und beschränke den Zugriff wenn möglich.

## Lizenz / License

Dieses Projekt steht unter der MIT-Lizenz. This project is licensed under the MIT License. Siehe [LICENSE](LICENSE) for details.
