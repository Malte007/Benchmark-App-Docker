# 🧪 Benchmark App

Die **Benchmark App** ist eine einfache Webanwendung auf Basis von **Flask** und **SQLite**, mit der sich Benchmark-Ergebnisse für verschiedene Systeme erfassen, verwalten und vergleichen lassen.
Dieses Projekt wurde mit Hilfe von chatGPT erstellt und bearbeitet.

## 🔧 Funktionen

- Systeme mit Hardwaredaten und Overclocking-Infos anlegen
- Benchmark-Typen erstellen (z. B. Cinebench, 3DMark etc.)
- Benchmark-Ergebnisse einem System und Typ zuordnen
- Ergebnisse werden automatisch absteigend nach Score sortiert

---

## 🧩 Voraussetzungen

### Lokale Ausführung (ohne Docker):

- Python 3.12+
- Pip (Python-Paketmanager)
- Empfohlen: venv für eine virtuelle Umgebung

### Docker-Ausführung:

- Docker Engine
- Docker Compose

---

## ▶️ Lokale Ausführung

### 1. Repository klonen

```bash
git clone https://github.com/dein-benutzername/benchmark-app.git
cd benchmark-app
```

### 2. Virtuelle Umgebung erstellen (optional, empfohlen)

```bash
python -m venv venv
source venv/bin/activate  # unter Windows: venv\Scripts\activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. App starten

```bash
python app.py
```

Die App ist dann unter [http://localhost:5000](http://localhost:5000) erreichbar.

---

## 🐳 Ausführung mit Docker

### 1. Datenbank-Zielordner erstellen (einmalig)

```bash
mkdir -p /my/host/path/to/db
```

> ⚠ Passe diesen Pfad ggf. an dein System an.

### 2. Docker-Umgebungsvariable setzen und Container starten

```bash
export DB_PATH=/my/host/path/to/db
docker-compose up --build
```
Alternativ mit .env-Datei:

#### .env

```bash
DB_PATH=/my/host/path/to/db
```

####  starten

```bash
docker-compose --env-file .env up --build
```

### 3. App im Browser öffnen

[http://localhost:5000](http://localhost:5000)

---

## 📁 Projektstruktur (Kurzüberblick)

```bash
.
├── app.py                  # Haupt-Flask-Anwendung
├── templates/              # HTML-Templates (Jinja2)
├── static/                 # Statische Dateien (CSS, JS – falls benötigt)
├── requirements.txt        # Python-Abhängigkeiten
├── Dockerfile              # Docker-Build-Anweisungen
└── docker-compose.yml      # Multi-Container-Konfiguration
```

---

## ✅ Hinweise

- Beim ersten Start wird automatisch eine SQLite-Datenbank (`benchmark.db`) erzeugt.
