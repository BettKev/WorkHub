# ai/agent.py
import logging
import requests
from typing import Optional, Dict, Any


class AIAgent:
    """
    AIAgent acts as the interface between the app and Google's Gemini AI API.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={api_key}"
            if api_key else None
        )

    def query_gemini(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Send a query to Gemini AI API and return the response text.
        """
        try:
            if not self.api_key or not self.base_url:
                # Stub response when no API key is provided
                return f"🤖 Gemini (stub): I received your message -> '{prompt}'"

            headers = {
                "Content-Type": "application/json",
                "X-goog-api-key": self.api_key  # explicit header like in curl
            }

            payload = {
                "contents": [
                    {
                        "parts": [{"text": prompt}]
                    }
                ]
            }

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
