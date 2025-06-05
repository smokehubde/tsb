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
* Verwaltung von Versandkosten pro Land.
* Nach Auswahl des Landes zeigt der Bot die Versandkosten an.
=======

* GUI läuft lokal auf Port 8000.
* Neue Route `/tor` ermöglicht das Steuern des Tor-Dienstes über die
  Variablen `ENABLE_TOR`, `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` und
  `TOR_CONTROL_PASS`.

## Setup

Für das Setup wird Python 3 benötigt. Auf manchen Systemen heißt das
Kommando `python3`.

### Schritt-für-Schritt-Anleitung

1. **Repository klonen**
   ```bash
   git clone https://example.com/tsb.git
   cd tsb
   ```
2. **Setup-Skript ausführen** – wähle je nach Plattform zwischen dem
   Bash-Skript oder der Python-Variante. Das Skript legt eine virtuelle
   Umgebung an, installiert alle Abhängigkeiten und fragt die benötigten
   Variablen ab:
   - `BOT_TOKEN` – das Telegram-Token deines Bots
   - `ADMIN_USER` – Benutzername für den Admin-Zugang
   - `ADMIN_PASS` – Passwort für den Admin-Zugang (wird gehasht gespeichert)
   - `SECRET_KEY` – geheimer Schlüssel für Flask
   - weitere optionale Einstellungen wie Datenbank-URL oder Webhook-Daten

   ```bash
   ./setup.sh [--no-services]  # Linux/macOS
   # oder
   python3 setup.py # Windows oder alternativ
   ```
   Die Werte werden in der Datei `.env` gespeichert und können dort später
   angepasst werden.
3. **Dienste starten** – auf Linux richten die Skripte automatisch
   systemd-Dienste ein und starten sie. Auf anderen Systemen startest du
   Bot und GUI manuell:
   ```bash
   python3 bot.py
   python3 admin_app.py
   ```
   Wenn du das Setup-Skript übersprungen hast oder die Programme außerhalb
   des Verzeichnisses `venv` ausführst, installiere zunächst die Abhängigkeiten
   mit:
   ```bash
   pip install -r requirements.txt
   ```

Die Skripte legen dabei eine virtuelle Umgebung unter `venv` an,
installieren die Abhängigkeiten und schreiben deine Angaben in die
Datei `.env`. Auf Linux werden zudem systemd-Dienste mit absoluten Pfaden
angelegt und sofort aktiviert:
```bash
systemctl --user daemon-reload
systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
```

Sollte `systemctl --user` nicht verfügbar sein, starte Bot und GUI manuell:
```bash
python3 bot.py
python3 admin_app.py
```


Nach dem Start ist der Bot über Telegram erreichbar (Token per
`BOT_TOKEN`-Umgebungsvariable setzen) und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).
Die Skripte schreiben Logdateien `bot.log` und `admin.log`, die bei Fehlern
hilfreich sind.
Nach dem Setup wird zudem eine Datei `onion_url.txt` mit der Tor-Adresse erzeugt,
die im Terminal ausgegeben wird. Stelle sicher, dass der Dienst `tor` läuft und
ein ControlPort (standardmäßig `9051`) erreichbar ist, sonst erscheint die Meldung
`Tor onion address not found`.

### So prüfst du dein Setup

Nach der Installation kannst du mit

```bash
pytest
```

sicherstellen, dass alle Tests erfolgreich durchlaufen.

## Umgebungsvariablen

Die systemd-Dienste laden ihre Konfiguration aus der Datei `.env`. Sie muss
die folgenden Variablen enthalten (eine Datei `.env.example` mit Musterwerten liegt bei):

* `BOT_TOKEN` – Telegram-Token für den Bot
* `ADMIN_USER` – Benutzername für das Admin-Login
* `ADMIN_PASS_HASH` – gehashter Passwort-Hash für den Admin-Login
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
* Manage shipping costs per country.
* After selecting the country the bot shows the shipping fee.
=======

* The GUI runs locally on port 8000.
* New `/tor` route allows controlling Tor using the `ENABLE_TOR`,
  `TOR_CONTROL_HOST`, `TOR_CONTROL_PORT` and `TOR_CONTROL_PASS`
  environment variables.

## Setup

Python 3 is required. On some systems the executable is named `python3`.

### Step-by-step

1. **Clone the repository**
   ```bash
   git clone https://example.com/tsb.git
   cd tsb
   ```
2. **Run the setup script** – choose the Bash or Python version depending on your platform. During setup you will be asked to enter:
   The script creates a virtual environment, installs all dependencies and prompts for
   the required values:
   - `BOT_TOKEN` – your Telegram bot token
   - `ADMIN_USER` – admin username
   - `ADMIN_PASS_HASH` – hashed admin password
   - `SECRET_KEY` – secret key for Flask
   - optional settings like database URL or webhook parameters

   ```bash
   ./setup.sh [--no-services]  # Linux/macOS
   # or
   python3 setup.py # Windows or alternative
   ```
   The answers are stored in `.env` and can be modified later.
3. **Start the services** – on Linux the scripts automatically configure and start
   systemd units. On other systems run the programs manually. Activate the
   virtual environment first so the installed dependencies are found:
   ```bash
   source venv/bin/activate
   python bot.py
   python admin_app.py
   ```
   If you skipped the setup script, install the requirements manually:
   ```bash
   ./venv/bin/pip install -r requirements.txt
   ```
   The scripts create a virtual environment under `venv`, install the dependencies and write your values to `.env`. On Linux, systemd units are enabled immediately using:
   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now "$REPO_DIR/bot.service" "$REPO_DIR/gui.service"
   ```

After starting, the bot is reachable via Telegram (set the token with the `BOT_TOKEN` environment variable) and the admin GUI is available at [http://localhost:8000](http://localhost:8000).
Log files `bot.log` and `admin.log` are created to help with troubleshooting.

The setup script also prints a Tor address stored in `onion_url.txt` to reach the GUI from anywhere. Ensure the `tor` service is running with a reachable control port (default `9051`), otherwise you will see `Tor onion address not found`.

### Verify your setup

After installing all requirements you can run

```bash
pytest
```

to ensure everything works as expected.

## Environment Variables

The systemd services load their configuration from the `.env` file. An example file `.env.example` is included. It must contain the following variables:

* `BOT_TOKEN` – Telegram token for the bot
* `ADMIN_USER` – Username for the admin login
* `ADMIN_PASS_HASH` – hashed password for the admin login
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
* `ONION_FILE` – file where the generated Tor URL is stored (default: `onion_url.txt`)


You can store these values in a `.env` file. This file must **not** be committed to the repository.

## Tests

Unit tests are executed using pytest. After installing the dependencies you can run them directly with `pytest`.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
