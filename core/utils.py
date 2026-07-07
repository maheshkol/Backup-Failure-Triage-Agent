"""
Application Utilities

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

import functools
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from services import app_logger


# ==========================================================
# Time
# ==========================================================

def current_timestamp() -> str:
    """
    Current timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ==========================================================
# Incident IDs
# ==========================================================

def generate_incident_id() -> str:
    """
    Generate unique incident ID.
    """

    return f"INC-{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}"


# ==========================================================
# Report IDs
# ==========================================================

def generate_report_id() -> str:
    """
    Generate report ID.
    """

    return f"RPT-{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}"


# ==========================================================
# Script Name
# ==========================================================

def generate_script_name(
    extension: str = "ps1",
) -> str:
    """
    Generate script filename.
    """

    return f"script_{datetime.now():%Y%m%d_%H%M%S}.{extension}"


# ==========================================================
# Directory
# ==========================================================

def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if it doesn't exist.
    """

    directory = Path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


# ==========================================================
# Load File
# ==========================================================

def load_text_file(path: str | Path) -> str:
    """
    Read UTF-8 text file.
    """

    path = Path(path)

    if not path.exists():

        raise FileNotFoundError(path)

    return path.read_text(
        encoding="utf-8",
    )


# ==========================================================
# Execution Timer
# ==========================================================

def timer(func):
    """
    Measure execution time.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start

        app_logger.info(
            f"{func.__name__} executed in "
            f"{elapsed:.2f} sec"
        )

        return result

    return wrapper


# ==========================================================
# Save File
# ==========================================================

def save_text_file(
    path: str | Path,
    text: str,
) -> Path:
    """
    Save UTF-8 text.
    """

    path = Path(path)

    ensure_directory(path.parent)

    path.write_text(
        text,
        encoding="utf-8",
    )

    return path


# ==========================================================
# UUID
# ==========================================================

def short_uuid() -> str:
    """
    Generate short UUID.
    """

    return uuid4().hex[:8].upper()