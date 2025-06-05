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
hilfreich sind. Die Dateien werden in dem Verzeichnis abgelegt, das in den
systemd-Service-Dateien als `WorkingDirectory` angegeben ist.
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


Nach dem Start ist der Bot über Telegram erreichbar und die Admin-GUI unter [http://localhost:8000](http://localhost:8000). Die Skripte schreiben Logdateien `bot.log` und `admin.log`. Nach dem Setup wird außerdem eine Datei `onion_url.txt` mit der Tor-Adresse erzeugt, sofern `tor` mit einem erreichbaren ControlPort (Standard `9051`) läuft.

After starting, the bot is reachable via Telegram (set the token with the `BOT_TOKEN` environment variable) and the admin GUI is available at [http://localhost:8000](http://localhost:8000).
Log files `bot.log` and `admin.log` are created to help with troubleshooting.
They are written to the directory configured as `WorkingDirectory` in the
service files.

The setup script also prints a Tor address stored in `onion_url.txt` to reach the GUI from anywhere. Ensure the `tor` service is running with a reachable control port (default `9051`), otherwise you will see `Tor onion address not found`.


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
