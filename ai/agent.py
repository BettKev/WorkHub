# ai/agent.py
import logging
import requests
from typing import Optional, Dict, Any


class AIAgent:
    """
    AIAgent acts as the interface between the app and Google's Gemini AI API.
    It injects context so responses are aligned with the purpose of the application.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={api_key}"
            if api_key else None
        )

        # Default global context for your app
        self.default_context = (
            "You are WorkHub AI, a helpful productivity assistant inside a desktop app. "
            "You help users manage tasks, projects, schedules, and team communication. "
            "Always keep answers short, practical, and relevant to workplace productivity."
        )

    def query_gemini(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Send a query to Gemini AI API with injected context.
        """
        try:
            if not self.api_key or not self.base_url:
                # Stub response when no API key is provided
                return f"🤖 Gemini (stub): Context='{self.default_context}' | Message='{prompt}'"

            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": self.api_key  # explicit header like in curl
            }

            # Correct structure: single contents array, multiple parts
            parts = [{"text": self.default_context}]
            if context:
                parts.append({"text": f"Additional context: {context}"})
            parts.append({"text": prompt})

            payload = {"contents": [{"parts": parts}]}

            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()

            # Extract the model's text response safely
            return (
                data.get("candidates", [{}])[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "🤖 (no reply from Gemini)")
            )

        except Exception as e:
            logging.exception("Gemini API call failed")
            return f"❌ API Error: {e}"
