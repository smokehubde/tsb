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

Das Projekt bietet zwei gleichwertige Skripte zum Einrichten der
Entwicklungsumgebung:

* `setup.sh` – Bash-Skript für Linux/macOS.
* `setup.py` – Python-Variante, die auch unter Windows funktioniert.

Beide Skripte legen eine virtuelle Umgebung im Ordner `venv` an, installieren
die Abhängigkeiten aus `requirements.txt`, schreiben die benötigten Variablen in
eine `.env`-Datei und erzeugen auf Linux die systemd-Dienste für Bot und GUI.

Unter Unix-Systemen führst du typischerweise das Shell-Skript aus:

```bash
./setup.sh
```

Auf allen Plattformen kannst du alternativ das Python-Skript verwenden:

```bash
python setup.py
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

Die Werte können beispielsweise in einer `.env`-Datei gespeichert werden.
Diese Datei darf **nicht** ins Repository eingecheckt werden.
