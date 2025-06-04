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

## Setup

Das Skript `setup.sh` richtet eine Python-`venv` ein, installiert die
Abhängigkeiten und erstellt systemd-Dienste für Bot und GUI.

```bash
./setup.sh
```

Das Skript liest `BOT_TOKEN`, `ADMIN_USER`, `ADMIN_PASS` und `SECRET_KEY`
aus einer `.env`-Datei im Projektverzeichnis. Fehlen dort Werte, wirst du zur
Eingabe aufgefordert und die Datei wird entsprechend aktualisiert.

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
