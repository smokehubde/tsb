# Telegram Shop Bot

Dieses Projekt beinhaltet einen einfachen Telegram-Bot und eine Admin-Oberfläche
zum Verwalten von Produkten. Der Bot ist mit aiogram 3.x umgesetzt, die
Admin-GUI basiert auf Flask.

## Funktionen

* Bot fragt bei `/start` die Sprache ab (Deutsch oder Englisch) und speichert
diese Einstellung für den Nutzer.
* Erste Menü-Ausgabe "Wähle ein Produkt" bzw. "Choose a product" je nach Sprache.
* Admin-Login (Benutzer und Passwort werden über Umgebungsvariablen
  `ADMIN_USER` und `ADMIN_PASS` gesetzt; Standard ist `admin`/`q12wq12w`).
* Produktverwaltung mit Name, Preis und Beschreibung.
* GUI läuft lokal auf Port 8000.

## Setup

Das Skript `setup.sh` richtet eine Python-`venv` ein, installiert die
Abhängigkeiten und versucht unter Linux systemd-Dienste für Bot und GUI
anzulegen. Auf anderen Plattformen erhält man Startbefehle, um die
Anwendungen manuell zu starten.

```bash
./setup.sh
```

Vor dem Start können Sie die Datei `.env.example` nach `.env` kopieren und die
benötigten Werte wie `BOT_TOKEN` oder Datenbank-URL anpassen. Nach der
Installation ist der Bot über Telegram erreichbar und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).
