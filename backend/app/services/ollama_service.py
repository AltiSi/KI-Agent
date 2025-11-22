import requests
from typing import Dict, List, Optional
from ..config import settings
import json


class OllamaAIService:
    """
    Kostenlose AI Service Implementation mit Ollama (lokal).
    Keine API Keys nötig, läuft komplett auf deinem Mac!
    """

    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # Oder "mistral", "llama2", etc.

    def _call_ollama(self, prompt: str, max_tokens: int = 2048) -> str:
        """Ruft Ollama API lokal auf."""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": 0.7
                    }
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                raise Exception(f"Ollama Error: {response.status_code}")

        except requests.exceptions.ConnectionError:
            raise Exception("Ollama ist nicht gestartet. Bitte 'ollama serve' ausführen.")
        except Exception as e:
            raise Exception(f"Ollama Fehler: {str(e)}")

    def analyze_document(self, document_text: str, filename: str) -> Dict:
        """
        Analysiert ein Dokument und extrahiert wichtige Informationen.
        """

        prompt = f"""Du bist ein freundlicher persönlicher Assistent. Analysiere dieses Dokument und extrahiere wichtige Informationen.

Dokument: {filename}
Inhalt:
{document_text}

Bitte analysiere das Dokument und gib mir folgende Informationen als JSON zurück:

{{
    "summary": "Eine kurze, einfache Zusammenfassung in 2-3 Sätzen",
    "important_info": "Die wichtigsten Informationen (Absender, Betreff, Beträge, etc.)",
    "category": "Eine Kategorie: Brief, Rechnung, Vertrag, Versicherung, Behörde, Gesundheit, oder Sonstiges",
    "deadlines": [
        {{"date": "YYYY-MM-DD", "description": "Was bis wann erledigt werden muss"}}
    ],
    "next_steps": [
        "Konkreter nächster Schritt 1",
        "Konkreter nächster Schritt 2"
    ],
    "tasks": [
        {{"title": "Aufgabe", "priority": "niedrig/mittel/hoch/dringend", "due_date": "YYYY-MM-DD oder null"}}
    ],
    "appointments": [
        {{"title": "Termin", "date": "YYYY-MM-DD HH:MM", "location": "Ort oder null"}}
    ]
}}

Wichtig:
- Schreibe in einfacher, verständlicher Sprache
- Erkenne Fristen, Zahlungen, Termine
- Antworte NUR mit dem JSON, ohne weitere Erklärungen
"""

        try:
            response_text = self._call_ollama(prompt, max_tokens=2048)

            # Extrahiere JSON aus der Antwort (manchmal gibt es extra Text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                result = json.loads(json_str)
                return result
            else:
                raise json.JSONDecodeError("Kein JSON gefunden", response_text, 0)

        except json.JSONDecodeError:
            # Fallback wenn JSON nicht geparst werden kann
            return {
                "summary": "Dokument hochgeladen. Analysiere es manuell.",
                "important_info": "Bitte Dokument manuell prüfen.",
                "category": "Sonstiges",
                "deadlines": [],
                "next_steps": ["Dokument manuell prüfen"],
                "tasks": [],
                "appointments": []
            }
        except Exception as e:
            print(f"Ollama AI Service Error: {str(e)}")
            return {
                "summary": f"Fehler bei der Analyse: {str(e)}",
                "important_info": "Stelle sicher, dass Ollama läuft: 'ollama serve'",
                "category": "Sonstiges",
                "deadlines": [],
                "next_steps": [],
                "tasks": [],
                "appointments": []
            }

    def get_daily_summary(self, tasks: List[Dict], appointments: List[Dict]) -> str:
        """
        Erstellt eine freundliche Zusammenfassung für den Tag.
        """

        prompt = f"""Du bist ein freundlicher persönlicher Assistent. Erstelle eine kurze, motivierende Zusammenfassung für den heutigen Tag.

Aufgaben für heute:
{json.dumps(tasks, ensure_ascii=False, indent=2)}

Termine für heute:
{json.dumps(appointments, ensure_ascii=False, indent=2)}

Erstelle eine freundliche, kurze Zusammenfassung (2-3 Sätze) mit:
- Was heute ansteht
- Prioritäten
- Ermutigende Worte

Schreibe in einem freundlichen, alltagsnahen Ton auf Deutsch.
"""

        try:
            response = self._call_ollama(prompt, max_tokens=512)
            return response.strip()
        except Exception as e:
            return f"Guten Tag! Du hast heute {len(tasks)} Aufgaben und {len(appointments)} Termine. 💪"

    def suggest_routine(self, habits_data: Optional[Dict] = None) -> List[str]:
        """
        Schlägt hilfreiche Routinen basierend auf Gewohnheiten vor.
        """

        prompt = """Du bist ein freundlicher persönlicher Assistent. Schlage 3-5 hilfreiche Alltagsroutinen vor,
die dabei helfen, organisiert und entspannt zu bleiben.

Beispiele:
- Morgenroutine: Tagesplanung nach dem Aufstehen
- Trinkerinnerung alle 2 Stunden
- Abends To-do-Liste für nächsten Tag vorbereiten

Gib die Vorschläge als JSON-Array auf Deutsch zurück:
["Routine 1", "Routine 2", "Routine 3"]
"""

        try:
            response = self._call_ollama(prompt, max_tokens=512)

            # Extrahiere JSON Array
            json_start = response.find('[')
            json_end = response.rfind(']') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                suggestions = json.loads(json_str)
                return suggestions
            else:
                raise json.JSONDecodeError("Kein JSON Array gefunden", response, 0)

        except:
            return [
                "Morgenroutine: Tagesplanung nach dem Aufstehen",
                "Trinkerinnerung alle 2 Stunden",
                "Abends To-do-Liste für nächsten Tag vorbereiten"
            ]


# Singleton Instance für Ollama
ollama_ai_service = OllamaAIService()
