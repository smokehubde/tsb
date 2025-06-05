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
   python3 run_bot.py
   python3 run_admin.py
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
python3 run_bot.py
python3 run_admin.py
```


Nach dem Start ist der Bot über Telegram erreichbar (Token per
`BOT_TOKEN`-Umgebungsvariable setzen) und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).
Die Skripte schreiben Logdateien `bot.log` und `admin.log` im
Projektverzeichnis (dem `WorkingDirectory` der systemd-Dienste), die bei Fehlern
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

## English Summary

Run `./setup.sh` (or `python setup.py` on Windows) to create the virtual
environment and collect configuration values. Start the services with
`python run_bot.py` and `python run_admin.py`. Log files `bot.log` and
`admin.log` are written to the project directory specified as
`WorkingDirectory` in the systemd service files. If Tor support is enabled, the
generated address is stored in `onion_url.txt`.

