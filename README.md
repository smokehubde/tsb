# Telegram Shop Bot

Dieses Projekt beinhaltet einen einfachen Telegram-Bot und eine Admin-Oberfläche
zum Verwalten von Produkten. Der Bot ist mit aiogram 3.x umgesetzt, die
Admin-GUI basiert auf Flask.

## Funktionen

* Bot fragt bei `/start` die Sprache ab (Deutsch oder Englisch) und speichert
diese Einstellung für den Nutzer.
* Erste Menü-Ausgabe "Wähle ein Produkt" bzw. "Choose a product" je nach Sprache.
* Admin-Login (Benutzer `admin`, Passwort `q12wq12w`; Werte über
  `ADMIN_USER` und `ADMIN_PASS` anpassbar).
* Produktverwaltung mit Name, Preis und Beschreibung.
* GUI läuft lokal auf Port 8000.

## Setup

Das Skript `setup.sh` richtet eine Python-`venv` ein, installiert die
Abhängigkeiten und – falls möglich – erstellt systemd-Dienste für Bot und GUI.

```bash
./setup.sh
```

Nach dem Start ist der Bot über Telegram erreichbar (Token per
`BOT_TOKEN`-Umgebungsvariable setzen) und die Admin-GUI unter
[http://localhost:8000](http://localhost:8000).
Die Datei `tsb.env` enthält Platzhalter für diese Variablen und wird beim
Setup automatisch angelegt.

### Manuelles Starten (macOS/Windows)

Auf Systemen ohne systemd müssen Bot und GUI manuell gestartet werden.
Installieren Sie zuerst die Abhängigkeiten:

```bash
python -m venv venv
source venv/bin/activate  # auf Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Legen Sie anschließend folgende Umgebungsvariablen fest:

```bash
export BOT_TOKEN=<Ihr-Token>
export ADMIN_USER=admin
export ADMIN_PASS=q12wq12w
```
Sie können diese Werte auch in der Datei `tsb.env` hinterlegen und
vor dem Start mit `source tsb.env` einlesen.

Starten Sie danach beide Programme jeweils in einem Terminal:

```bash
python bot.py
python admin_app.py
```
