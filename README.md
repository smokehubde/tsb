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

Vor dem Ausführen sollte die Datei `.env.example` nach `.env` kopiert und die Werte angepasst werden.

```bash
./setup.sh
```

Das Skript fragt nach den notwendigen Variablen, falls diese nicht bereits in der
Umgebung gesetzt sind.

Nach dem Start ist der Bot über Telegram erreichbar (Token per
`BOT_TOKEN`-Umgebungsvariable setzen) und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).

## Umgebungsvariablen

Folgende Variablen müssen für die Dienste gesetzt sein:

* `BOT_TOKEN` – Telegram-Token für den Bot
* `DATABASE_URL` – Datenbank-URL für SQLAlchemy (z.B. `sqlite:///db.sqlite3`)
* `FLASK_SECRET_KEY` – Secret Key für Flask-Sitzungen
* `ADMIN_USER` – Benutzername für das Admin-Login
* `ADMIN_PASS` – Passwort für das Admin-Login
