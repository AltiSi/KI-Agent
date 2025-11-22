# 📌 Persönlicher Alltags- & Dokumenten-Assistent

Ein intelligenter, KI-gestützter Assistent für deinen Alltag – hilft dir dabei, Dokumente zu verwalten, Termine zu planen und dein Leben organisiert zu führen.

## ✨ Features

### 📄 Dokumente & Briefe
- Upload und automatische Analyse von Dokumenten (PDF, Word, Bilder)
- Intelligente Zusammenfassungen in einfacher Sprache
- Erkennung wichtiger Daten: Fristen, Zahlungen, Termine
- Ableitung konkreter nächster Schritte

### 📅 Termin- & Aufgabenplanung
- Automatische Extraktion von Terminen aus Dokumenten
- Aufgabenverwaltung mit Prioritäten
- Fristen-Erinnerungen
- Übersichtlicher Kalender

### 🏠 Alltagshilfe
- Einkaufslisten
- Tages- und Wochenpläne
- Erinnerungen (Medikamente, Trinken, etc.)
- Gewohnheits-Tracking

## 🚀 Installation

### Voraussetzungen
- Python 3.9+
- Node.js 18+
- Claude API Key (von [Anthropic Console](https://console.anthropic.com/))
- Optional: Tesseract OCR für Bild-Texterkennung (`sudo apt-get install tesseract-ocr tesseract-ocr-deu` auf Linux)

### Backend starten

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# .env Datei erstellen und ANTHROPIC_API_KEY eintragen
cp .env.example .env
# Öffne .env und trage deinen API Key ein:
# ANTHROPIC_API_KEY=sk-ant-your-key-here

# Server starten
uvicorn app.main:app --reload
```

Backend läuft auf: `http://localhost:8000`

### Frontend starten

```bash
cd frontend
npm install
npm run dev
```

Frontend läuft auf: `http://localhost:5173`

## 📖 Verwendung

### Dokumente hochladen und analysieren

1. Öffne die App im Browser
2. Lade ein Dokument hoch (PDF, Word, Bild)
3. Der Assistent analysiert es automatisch und zeigt:
   - Einfache Zusammenfassung
   - Wichtige Informationen
   - Fristen & Termine
   - Empfohlene nächste Schritte
4. Aufgaben werden automatisch zur To-do-Liste hinzugefügt

### Weitere Funktionen

- **Aufgabenverwaltung**: Erstelle, bearbeite und verwalte Aufgaben mit Prioritäten
- **Terminkalender**: Verwalte deine Termine mit Datum, Uhrzeit und Ort
- **Einkaufslisten**: Erstelle Listen und hake erledigte Items ab
- **Erinnerungen**: Setze wiederkehrende oder einmalige Erinnerungen
- **Dashboard**: Übersicht über anstehende Aufgaben und Termine mit KI-Zusammenfassung

## 🛠 Technologie-Stack

- **Backend**: FastAPI, SQLAlchemy, Claude API, PyPDF2, python-docx, pytesseract
- **Frontend**: React, TypeScript, Tailwind CSS, React Router
- **Datenbank**: SQLite
- **KI**: Anthropic Claude

## 📝 Lizenz

MIT
