"""
Log Parser

Parses Veeam-style backup logs and extracts
structured information for the Incident Analysis Agent.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

import re
from pathlib import Path
from typing import Dict, Optional

from services import app_logger


class LogParser:
    """
    Parse backup log files into structured data.
    """

    # -------------------------
    # Regular Expressions
    # -------------------------

    JOB_PATTERN = re.compile(
        r"Job\s*Name\s*:\s*(.+)",
        re.IGNORECASE,
    )

    VM_PATTERN = re.compile(
        r"VM\s*Name\s*:\s*(.+)",
        re.IGNORECASE,
    )

    REPOSITORY_PATTERN = re.compile(
        r"Repository\s*:\s*(.+)",
        re.IGNORECASE,
    )

    ERROR_PATTERN = re.compile(
        r"Error\s*:\s*(.+)",
        re.IGNORECASE,
    )

    ERROR_CODE_PATTERN = re.compile(
        r"Error\s*Code\s*:\s*(.+)",
        re.IGNORECASE,
    )

    TIME_PATTERN = re.compile(
        r"(Start Time|Time)\s*:\s*(.+)",
        re.IGNORECASE,
    )

    # --------------------------------------------

    def parse_file(self, file_path: str) -> Dict:
        """
        Parse a log file.

        Args:
            file_path: Path to the log file.

        Returns:
            Dictionary containing parsed values.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(path)

        app_logger.info(f"Parsing log file: {path}")

        text = path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        return self.parse_text(text)

    # --------------------------------------------

    def parse_text(self, log_text: str) -> Dict:
        """
        Parse raw log text.

        Returns:
            Dictionary containing extracted fields.
        """

        result = {
            "job_name": self._search(
                self.JOB_PATTERN,
                log_text,
            ),
            "vm_name": self._search(
                self.VM_PATTERN,
                log_text,
            ),
            "repository": self._search(
                self.REPOSITORY_PATTERN,
                log_text,
            ),
            "error": self._search(
                self.ERROR_PATTERN,
                log_text,
            ),
            "error_code": self._search(
                self.ERROR_CODE_PATTERN,
                log_text,
            ),
            "timestamp": self._search(
                self.TIME_PATTERN,
                log_text,
                group=2,
            ),
            "severity": self.detect_severity(log_text),
            "failure_type": self.detect_failure_type(log_text),
            "raw_log": log_text,
        }

        app_logger.info(
            f"Log parsed successfully. Failure Type: {result['failure_type']}"
        )

        return result

    # --------------------------------------------

    @staticmethod
    def _search(
        pattern: re.Pattern,
        text: str,
        group: int = 1,
    ) -> Optional[str]:

        match = pattern.search(text)

        if match:
            return match.group(group).strip()

        return None

    # --------------------------------------------

    @staticmethod
    def detect_severity(text: str) -> str:

        text = text.lower()

        if any(
            word in text
            for word in [
                "critical",
                "fatal",
                "repository full",
                "disk full",
            ]
        ):
            return "Critical"

        if any(
            word in text
            for word in [
                "timeout",
                "snapshot",
                "permission denied",
                "access denied",
            ]
        ):
            return "High"

        return "Medium"

    # --------------------------------------------

    @staticmethod
    def detect_failure_type(text: str) -> str:

        text = text.lower()

        patterns = {

            "Repository Full": [
                "repository full",
                "disk full",
                "no space left",
            ],

            "Network Timeout": [
                "timeout",
                "connection lost",
                "network",
            ],

            "Snapshot Locked": [
                "snapshot",
                "locked",
            ],

            "Credential Failure": [
                "access denied",
                "permission denied",
                "authentication failed",
            ],

            "Agent Unreachable": [
                "agent unreachable",
                "cannot connect",
            ],

            "Unknown": [],
        }

        for failure, keywords in patterns.items():

            for keyword in keywords:

                if keyword in text:
                    return failure

        return "Unknown"


# Singleton

log_parser = LogParser()