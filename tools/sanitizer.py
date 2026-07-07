"""
Log Sanitizer

Removes or masks sensitive information before
sending backup logs to the LLM.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

import re

from services import app_logger


class LogSanitizer:
    """
    Sanitizes backup logs by masking sensitive information.
    """

    def __init__(self):

        self.patterns = [

            # IPv4 Addresses
            (
                re.compile(
                    r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
                ),
                "[REDACTED_IP]",
            ),

            # Email Address
            (
                re.compile(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
                ),
                "[REDACTED_EMAIL]",
            ),

            # URLs
            (
                re.compile(
                    r"https?://[^\s]+"
                ),
                "[REDACTED_URL]",
            ),

            # Windows Paths
            (
                re.compile(
                    r"[A-Za-z]:\\(?:[^\\\n]+\\)*[^\\\n]*"
                ),
                "[REDACTED_PATH]",
            ),

            # Linux Paths
            (
                re.compile(
                    r"/(?:[\w.-]+/)*[\w.-]+"
                ),
                "[REDACTED_PATH]",
            ),

            # Password
            (
                re.compile(
                    r"(password\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED]",
            ),

            # Username
            (
                re.compile(
                    r"(username\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED]",
            ),

            # API Key
            (
                re.compile(
                    r"(api[_-]?key\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED]",
            ),

            # Token
            (
                re.compile(
                    r"(token\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED]",
            ),

            # Authorization Header
            (
                re.compile(
                    r"(authorization\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED]",
            ),

            # Hostname
            (
                re.compile(
                    r"(hostname\s*[:=]\s*)(.+)",
                    re.IGNORECASE,
                ),
                r"\1[REDACTED_HOST]",
            ),
        ]

    # -------------------------------------------------

    def sanitize(self, log_text: str) -> str:
        """
        Remove sensitive information.

        Args:
            log_text: Raw log

        Returns:
            Sanitized log
        """

        sanitized = log_text

        replacements = 0

        for pattern, replacement in self.patterns:

            sanitized, count = pattern.subn(
                replacement,
                sanitized,
            )

            replacements += count

        app_logger.info(
            f"Log sanitized. {replacements} sensitive values masked."
        )

        return sanitized

    # -------------------------------------------------

    def has_sensitive_data(self, log_text: str) -> bool:
        """
        Returns True if sensitive data is detected.
        """

        for pattern, _ in self.patterns:

            if pattern.search(log_text):
                return True

        return False


# Singleton

log_sanitizer = LogSanitizer()