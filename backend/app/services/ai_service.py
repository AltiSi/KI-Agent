from anthropic import Anthropic
from typing import Dict, List, Optional
from ..config import settings
import json


class AIService:
    def __init__(self):
        self._client = None
        self.model = "claude-3-5-sonnet-20241022"

    @property
    def client(self):
        """Lazy initialization of Anthropic client."""
        if self._client is None:
            self._client = Anthropic(api_key=settings.anthropic_api_key)
        return self._client

    def analyze_document(self, document_text: str, filename: str) -> Dict:
        """
        Analysiert ein Dokument und extrahiert wichtige Informationen.

        Returns:
            {
                "summary": "Einfache Zusammenfassung",
                "important_info": "Wichtige Informationen",
                "category": "Brief/Rechnung/etc.",
                "deadlines": [{"date": "2024-03-15", "description": "Formular abschicken"}],
                "next_steps": ["Schritt 1", "Schritt 2"],
                "tasks": [{"title": "...", "priority": "hoch", "due_date": "..."}],
                "appointments": [{"title": "...", "date": "...", "location": "..."}]
            }
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
- Wenn etwas nicht sicher ist, schreibe "unklar" oder lasse es weg
- Sei konkret bei den nächsten Schritten
- Antworte NUR mit dem JSON, ohne weitere Erklärungen
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            # Parse JSON response
            result = json.loads(response_text)
            return result

        except json.JSONDecodeError:
            # Fallback wenn JSON nicht geparst werden kann
            return {
                "summary": "Dokument hochgeladen, aber Analyse fehlgeschlagen.",
                "important_info": "Bitte Dokument manuell prüfen.",
                "category": "Sonstiges",
                "deadlines": [],
                "next_steps": ["Dokument manuell prüfen"],
                "tasks": [],
                "appointments": []
            }
        except Exception as e:
            print(f"AI Service Error: {str(e)}")
            return {
                "summary": f"Fehler bei der Analyse: {str(e)}",
                "important_info": "",
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

Schreibe in einem freundlichen, alltagsnahen Ton.
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            return message.content[0].text

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

Gib die Vorschläge als JSON-Array zurück:
["Routine 1", "Routine 2", "Routine 3"]
"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=512,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text
            suggestions = json.loads(response_text)
            return suggestions

        except:
            return [
                "Morgenroutine: Tagesplanung nach dem Aufstehen",
                "Trinkerinnerung alle 2 Stunden",
                "Abends To-do-Liste für nächsten Tag vorbereiten"
            ]


# Singleton Instance
ai_service = AIService()
