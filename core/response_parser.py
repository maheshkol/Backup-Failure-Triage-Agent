"""
Response Parser

Safely parses and validates LLM responses into
Pydantic models.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

import json
import re
from typing import Any, Type, TypeVar

from pydantic import BaseModel, ValidationError

from services import app_logger

from .exceptions import AgentExecutionError

T = TypeVar("T", bound=BaseModel)


class ResponseParser:
    """
    Parses LLM responses into structured models.
    """

    # ==========================================================
    # Public Methods
    # ==========================================================

    def parse(
        self,
        response: str,
        model: Type[T],
    ) -> T:
        """
        Convert an LLM response into a validated Pydantic model.
        """

        cleaned = self.clean_response(response)

        json_data = self.extract_json(cleaned)

        return self.validate(json_data, model)

    # ==========================================================

    def clean_response(
        self,
        response: str,
    ) -> str:
        """
        Remove markdown formatting and whitespace.
        """

        if not response:

            raise AgentExecutionError(
                "Empty response received from Gemini."
            )

        response = response.strip()

        # Remove ```json
        response = re.sub(
            r"^```json",
            "",
            response,
            flags=re.IGNORECASE,
        )

        # Remove ```
        response = re.sub(
            r"```$",
            "",
            response,
            flags=re.MULTILINE,
        )

        return response.strip()

    # ==========================================================

    def extract_json(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Extract JSON from an LLM response.
        """

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            pass

        match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL,
        )

        if match:

            try:

                return json.loads(match.group())

            except Exception:

                pass

        app_logger.error("Invalid JSON received from Gemini.")

        raise AgentExecutionError(
            "Gemini returned invalid JSON."
        )

    # ==========================================================

    def validate(
        self,
        data: dict[str, Any],
        model: Type[T],
    ) -> T:
        """
        Validate JSON against a Pydantic model.
        """

        try:

            result = model.model_validate(data)

            app_logger.success(
                f"{model.__name__} validated successfully."
            )

            return result

        except ValidationError as ex:

            app_logger.exception(ex)

            raise AgentExecutionError(
                f"Validation failed for {model.__name__}"
            ) from ex

    # ==========================================================

    def pretty_json(
        self,
        model: BaseModel,
    ) -> str:
        """
        Pretty-print a model as JSON.
        """

        return model.model_dump_json(
            indent=4
        )

    # ==========================================================

    def to_dict(
        self,
        model: BaseModel,
    ) -> dict[str, Any]:
        """
        Convert model to dictionary.
        """

        return model.model_dump()


# ==========================================================
# Singleton
# ==========================================================

response_parser = ResponseParser()