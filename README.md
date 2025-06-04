# Telegram Shop Bot

Dieses Projekt beinhaltet einen einfachen Telegram-Bot und eine Admin-Oberfläche
zum Verwalten von Produkten. Der Bot ist mit aiogram 3.x umgesetzt, die
Admin-GUI basiert auf Flask.

## Funktionen

* Bot fragt bei `/start` die Sprache ab (Deutsch oder Englisch) und speichert
diese Einstellung für den Nutzer.
* Erste Menü-Ausgabe "Wähle ein Produkt" bzw. "Choose a product" je nach Sprache.
* Admin-Login (Benutzername und Passwort über `ADMIN_USER` und `ADMIN_PASS`).
* Produktverwaltung mit Name, Preis und Beschreibung.
* GUI läuft lokal auf Port 8000.
* Neue Route `/tor` ermöglicht das Steuern des Tor-Dienstes über die
  Variablen `ENABLE_TOR`, `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` und
  `TOR_CONTROL_PASS`.

## Setup

Für das Setup wird Python 3 benötigt. Auf manchen Systemen heißt das
Kommando `python3`.

Das Projekt bietet zwei gleichwertige Skripte zum Einrichten der
Entwicklungsumgebung:

* `setup.sh` – Bash-Skript für Linux/macOS.
* `setup.py` – Python-Variante, die auch unter Windows funktioniert.

Beide Skripte legen eine virtuelle Umgebung im Ordner `venv` an, installieren
die Abhängigkeiten aus `requirements.txt`, schreiben die benötigten Variablen in
eine `.env`-Datei und erzeugen auf Linux die systemd-Dienste für Bot und GUI.
Die Dienste werden dabei mit absoluten Pfaden aktiviert:
`systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"`.
Zuvor wird automatisch `systemctl --user daemon-reload` ausgeführt.

Unter Unix-Systemen führst du typischerweise das Shell-Skript aus:

```bash
./setup.sh
```

Auf allen Plattformen kannst du alternativ das Python-Skript verwenden:

```bash
python3 setup.py
```

Sollte `systemctl --user` nicht verfügbar sein, starte Bot und GUI manuell:

```bash
python3 bot.py
python3 admin_app.py
```


Nach dem Start ist der Bot über Telegram erreichbar (Token per
`BOT_TOKEN`-Umgebungsvariable setzen) und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).

## Umgebungsvariablen

Die systemd-Dienste laden ihre Konfiguration aus der Datei `.env`. Sie muss
die folgenden Variablen enthalten:

* `BOT_TOKEN` – Telegram-Token für den Bot
* `ADMIN_USER` – Benutzername für das Admin-Login
* `ADMIN_PASS` – Passwort für das Admin-Login
* `SECRET_KEY` – Flask-`SECRET_KEY` für die Web-Oberfläche
* `DATABASE_URL` – optionale Datenbank-URL (Standard: `sqlite:///db.sqlite3`)
* `ADMIN_HOST` – Hostname/IP für die Admin-GUI (Standard: `127.0.0.1`)
* `ADMIN_PORT` – Port der Admin-GUI (Standard: `8000`)
* `WEBHOOK_URL` – HTTPS-URL für Telegram-Webhooks (optional)
* `WEBHOOK_HOST` – Hostname/IP für den Webhook-Server (Standard: `0.0.0.0`)
* `WEBHOOK_PORT` – Port für den Webhook-Server (Standard: `8080`)
* `WEBHOOK_PATH` – Pfad der Webhook-Route (Standard: `/webhook`)


Die Werte können beispielsweise in einer `.env`-Datei gespeichert werden.
Diese Datei darf **nicht** ins Repository eingecheckt werden.

### Sicherheitshinweise

Wird `ADMIN_HOST` auf `0.0.0.0` gesetzt oder der Tor-Dienst aktiviert, ist die
Admin-Oberfläche von außen erreichbar. Verwende ein starkes Passwort und
beschränke den Zugriff nach Möglichkeit weiter.

## Tests

Die Unit-Tests werden mit pytest ausgeführt. Nach dem Installieren der Abhängigkeiten kannst du sie direkt mit `pytest` ausführen.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) fuer Details.

---

# Telegram Shop Bot (English)

This project contains a simple Telegram bot and an admin interface for managing products. The bot uses aiogram 3.x and the admin GUI is built with Flask.

## Features

* On `/start` the bot asks for the language (German or English) and stores the setting for the user.
* The first menu shows "Wähle ein Produkt" or "Choose a product" depending on the chosen language.
* Admin login using the username and password from `ADMIN_USER` and `ADMIN_PASS`.
* Manage products with name, price and description.
* The GUI runs locally on port 8000.
* New `/tor` route allows controlling Tor using the `ENABLE_TOR`,
  `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` and `TOR_CONTROL_PASS`
  environment variables.

## Setup

Python 3 is required. On some systems the executable is named `python3`.

The project provides two equivalent scripts for setting up the development environment:

* `setup.sh` – Bash script for Linux/macOS.
* `setup.py` – Python variant that also works on Windows.

Both scripts create a virtual environment in the `venv` folder, install the dependencies from `requirements.txt`, write the required variables to a `.env` file and on Linux create the systemd services for bot and GUI. The services are enabled using absolute paths:
`systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"`. `systemctl --user daemon-reload` is executed automatically before enabling them.

On Unix systems you typically run the shell script:

```bash
./setup.sh
```

On any platform you can alternatively use the Python script:

```bash
python3 setup.py
```

If `systemctl --user` is not available, start bot and GUI manually:

```bash
python3 bot.py
python3 admin_app.py
```

After starting, the bot is reachable via Telegram (set the token with the `BOT_TOKEN` environment variable) and the admin GUI is available at [http://localhost:8000](http://localhost:8000).

## Environment Variables

The systemd services load their configuration from the `.env` file. It must contain the following variables:

* `BOT_TOKEN` – Telegram token for the bot
* `ADMIN_USER` – Username for the admin login
* `ADMIN_PASS` – Password for the admin login
* `SECRET_KEY` – Flask `SECRET_KEY` for the web interface
* `DATABASE_URL` – optional database URL (default: `sqlite:///db.sqlite3`)
* `ADMIN_HOST` – Hostname/IP for the admin GUI (default: `127.0.0.1`)
* `ADMIN_PORT` – Port of the admin GUI (default: `8000`)
* `WEBHOOK_URL` – HTTPS URL for Telegram webhooks (optional)
* `WEBHOOK_HOST` – Hostname/IP for the webhook server (default: `0.0.0.0`)
* `WEBHOOK_PORT` – Port for the webhook server (default: `8080`)
* `WEBHOOK_PATH` – Path for the webhook route (default: `/webhook`)
* `ENABLE_TOR` – set to `1` to expose the admin GUI via Tor
* `TOR_CONTROL_HOST` – host of the Tor control port (default: `127.0.0.1`)
* `TOR_CONTROL_PORT` – port of the Tor control port (default: `9051`)
* `TOR_CONTROL_PASS` – password for the Tor control port


You can store these values in a `.env` file. This file must **not** be committed to the repository.

## Tests

Unit tests are executed using pytest. After installing the dependencies you can run them directly with `pytest`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
