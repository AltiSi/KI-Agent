# 🆓 Ollama Setup - Kostenlose KI für deinen Assistenten

Ollama ist eine **100% kostenlose** Alternative zu Claude API. Die KI läuft **lokal auf deinem Mac** - komplett privat und offline!

## ✅ Vorteile von Ollama

- 💰 **Kostenlos** - Keine API Keys, keine Gebühren
- 🔒 **Privat** - Deine Dokumente bleiben auf deinem Mac
- 🌐 **Offline** - Funktioniert ohne Internet
- ⚡ **Schnell** - Läuft direkt auf deiner Hardware

---

## 📥 Installation (Mac)

### Option 1: Mit Homebrew (empfohlen)

```bash
brew install ollama
```

### Option 2: Download

1. Gehe zu https://ollama.ai/download
2. Lade "Ollama for macOS" herunter
3. Installiere die App

---

## 🚀 Schnellstart

### 1. Ollama starten

```bash
# Ollama Server starten
ollama serve
```

Lass dieses Terminal-Fenster offen! Ollama läuft im Hintergrund.

### 2. Modell herunterladen

**Öffne ein NEUES Terminal** und führe aus:

```bash
# Kleines, schnelles Modell (empfohlen für Anfang)
ollama pull llama3.2

# ODER: Größeres Modell für bessere Qualität
ollama pull mistral

# ODER: Deutschsprachiges Modell
ollama pull llama2:7b
```

**Tipp:** `llama3.2` ist ein guter Kompromiss zwischen Geschwindigkeit und Qualität!

### 3. Testen ob es funktioniert

```bash
ollama list
```

Du solltest deine installierten Modelle sehen.

**Test-Chat:**
```bash
ollama run llama3.2
>>> Hallo, wie geht es dir?
```

Wenn du eine Antwort bekommst → **Ollama funktioniert!** ✅

Zum Beenden: `/bye`

---

## ⚙️ App-Konfiguration

### .env Datei anpassen

```bash
cd backend
nano .env  # oder: open .env
```

**Stelle sicher, dass steht:**
```env
AI_PROVIDER=ollama
OLLAMA_MODEL=llama3.2
```

**Das wars!** 🎉

---

## 🎮 App starten

### Terminal 1: Ollama
```bash
ollama serve
```

### Terminal 2: Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

### Terminal 3: Frontend
```bash
cd frontend
npm run dev
```

Öffne im Browser: **http://localhost:5173**

---

## 🔄 Modell wechseln

Du kannst jederzeit das Modell wechseln:

```bash
# Andere Modelle herunterladen
ollama pull mistral
ollama pull llama2
ollama pull codellama

# In .env ändern:
OLLAMA_MODEL=mistral
```

Backend neu starten, fertig!

---

## 📊 Verfügbare Modelle

| Modell | Größe | Geschwindigkeit | Qualität | Empfohlen für |
|--------|-------|----------------|----------|---------------|
| `llama3.2` | ~2GB | ⚡⚡⚡ Sehr schnell | ⭐⭐⭐ Gut | **Alltag** ✅ |
| `mistral` | ~4GB | ⚡⚡ Schnell | ⭐⭐⭐⭐ Sehr gut | Bessere Analysen |
| `llama2:13b` | ~7GB | ⚡ Mittel | ⭐⭐⭐⭐⭐ Exzellent | Beste Qualität |
| `codellama` | ~4GB | ⚡⚡ Schnell | ⭐⭐⭐⭐ Sehr gut | Code-Analyse |

**Tipp:** Starte mit `llama3.2` - es ist schnell und gut genug für die meisten Aufgaben!

---

## 🆘 Problemlösung

### "Connection refused"
→ Ollama läuft nicht. Starte: `ollama serve`

### "Model not found"
→ Modell nicht heruntergeladen. Führe aus: `ollama pull llama3.2`

### Langsame Antworten
→ Nutze ein kleineres Modell: `ollama pull llama3.2`

### Ollama nicht gefunden
→ Neu installieren: `brew install ollama`

---

## 🔄 Zurück zu Claude wechseln

Falls du später doch Claude nutzen möchtest:

```env
# In .env ändern:
AI_PROVIDER=claude
ANTHROPIC_API_KEY=dein-echter-key
```

Backend neu starten, fertig!

---

## 💡 Tipps

- **Erster Start dauert länger** - Modell muss laden
- **Mac braucht genug RAM** - Mindestens 8GB empfohlen
- **M1/M2/M3 Macs** sind deutlich schneller
- **Ollama im Hintergrund lassen** - dann ist es immer bereit

---

**Viel Spaß mit deinem kostenlosen KI-Assistenten!** 🎉
