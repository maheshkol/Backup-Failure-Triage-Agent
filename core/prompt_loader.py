"""
Prompt Loader

Loads, caches, validates and renders prompt templates.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from pathlib import Path
from string import Template
from typing import Dict

from services import app_logger

from .exceptions import PromptNotFoundError


class PromptLoader:
    """
    Loads prompt templates from the prompts directory.

    Prompts are cached after first read to improve performance.
    """

    def __init__(self, prompt_directory: str = "prompts"):

        self.prompt_directory = Path(prompt_directory)

        self._cache: Dict[str, str] = {}

    # =====================================================
    # Private Methods
    # =====================================================

    def _get_prompt_path(self, prompt_name: str) -> Path:
        """
        Returns the path to a prompt file.
        """

        return self.prompt_directory / f"{prompt_name}.txt"

    # =====================================================

    def _read_prompt(self, prompt_name: str) -> str:
        """
        Reads a prompt from disk.
        """

        prompt_path = self._get_prompt_path(prompt_name)

        if not prompt_path.exists():

            raise PromptNotFoundError(
                f"Prompt '{prompt_name}' not found.\n"
                f"Expected: {prompt_path}"
            )

        app_logger.info(f"Loading prompt: {prompt_name}")

        return prompt_path.read_text(
            encoding="utf-8"
        )

    # =====================================================
    # Public Methods
    # =====================================================

    def load(self, prompt_name: str) -> str:
        """
        Load a prompt.

        Uses cache if already loaded.
        """

        if prompt_name not in self._cache:

            self._cache[prompt_name] = self._read_prompt(
                prompt_name
            )

        return self._cache[prompt_name]

    # =====================================================

    def reload(self, prompt_name: str) -> str:
        """
        Force reload prompt from disk.
        """

        app_logger.info(
            f"Reloading prompt: {prompt_name}"
        )

        self._cache[prompt_name] = self._read_prompt(
            prompt_name
        )

        return self._cache[prompt_name]

    # =====================================================

    def clear_cache(self):
        """
        Clear all cached prompts.
        """

        self._cache.clear()

        app_logger.info("Prompt cache cleared.")

    # =====================================================

    def available_prompts(self):
        """
        Returns all prompt names.
        """

        if not self.prompt_directory.exists():

            return []

        return sorted([
            file.stem
            for file in self.prompt_directory.glob("*.txt")
        ])

    # =====================================================

    def render(
        self,
        prompt_name: str,
        **kwargs,
    ) -> str:
        """
        Render prompt with variables.

        Example:

        ${log}

        ${incident}

        ${root_cause}
        """

        prompt = self.load(prompt_name)

        template = Template(prompt)

        return template.safe_substitute(**kwargs)

    # =====================================================

    def validate(self) -> bool:
        """
        Validate prompt directory.
        """

        required = [
            "incident_prompt",
            "remediation_prompt",
            "report_prompt",
        ]

        missing = []

        for prompt in required:

            if prompt not in self.available_prompts():

                missing.append(prompt)

        if missing:

            raise PromptNotFoundError(
                f"Missing prompts: {missing}"
            )

        app_logger.info(
            "Prompt validation successful."
        )

        return True


# ==========================================================
# Singleton
# ==========================================================

prompt_loader = PromptLoader()