"""
Gemini Service

Centralized Google Gemini client used by all agents.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from typing import Optional

import google.generativeai as genai

from config import settings
from services import app_logger


class GeminiService:
    """
    Wrapper around the Google Gemini API.
    """

    def __init__(self):
        self.model_name = settings.gemini_model

        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please configure it in your .env file."
            )

        genai.configure(api_key=settings.gemini_api_key)

        self.model = genai.GenerativeModel(self.model_name)

        app_logger.info(f"Gemini initialized with model: {self.model_name}")

    def generate(
        self,
        prompt: str,
        temperature: float = 0.2,
        max_output_tokens: int = 2048,
    ) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: User prompt
            temperature: Model creativity
            max_output_tokens: Maximum response length

        Returns:
            Generated text
        """

        try:

            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )

            text = response.text.strip()

            app_logger.info("Gemini response generated successfully.")

            return text

        except Exception as ex:
            app_logger.exception("Gemini API call failed.")
            raise RuntimeError(str(ex)) from ex

    def health_check(self) -> bool:
        """
        Simple health check.

        Returns:
            True if Gemini is reachable.
        """

        try:

            self.generate(
                "Reply with only the word OK.",
                temperature=0,
                max_output_tokens=5,
            )

            return True

        except Exception:

            return False


# Singleton Instance
gemini_service = GeminiService()