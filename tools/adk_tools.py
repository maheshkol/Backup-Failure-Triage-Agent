"""
ADK Tools

Exposes business functions as tools for Google ADK Agents.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""
from config import settings
from pathlib import Path
from typing import Any

from services import app_logger
from tools.log_parser import log_parser
from tools.sanitizer import log_sanitizer


# ==========================================================
# Parse Log Tool
# ==========================================================

def parse_backup_log(log_path: str) -> dict[str, Any]:
    """
    Parse a backup log file.

    Args:
        log_path: Path to backup log

    Returns:
        Structured log information
    """

    app_logger.info(f"ADK Tool -> Parsing {log_path}")

    try:

        result = log_parser.parse_file(log_path)

        return {
            "success": True,
            "message": "Log parsed successfully.",
            "data": result,
        }

    except Exception as ex:

        app_logger.exception(ex)

        return {
            "success": False,
            "message": str(ex),
            "data": None,
        }


# ==========================================================
# Sanitize Tool
# ==========================================================

def sanitize_backup_log(log_text: str) -> dict[str, Any]:
    """
    Remove sensitive information from backup logs.
    """

    app_logger.info("ADK Tool -> Sanitizing Log")

    try:

        sanitized = log_sanitizer.sanitize(log_text)

        return {
            "success": True,
            "message": "Log sanitized successfully.",
            "data": sanitized,
        }

    except Exception as ex:

        app_logger.exception(ex)

        return {
            "success": False,
            "message": str(ex),
            "data": None,
        }


# ==========================================================
# Save Markdown Report
# ==========================================================

def save_incident_report(
    filename: str,
    markdown: str,
) -> dict[str, Any]:
    """
    Save markdown report.
    """

    try:

        #report_dir = Path("reports/generated")
        report_dir = Path(settings.report_output_dir) 

        report_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_path = report_dir / filename

        report_path.write_text(
            markdown,
            encoding="utf-8",
        )

        app_logger.success(f"Report saved -> {report_path}")

        return {
            "success": True,
            "message": "Report saved.",
            "data": str(report_path),
        }

    except Exception as ex:

        app_logger.exception(ex)

        return {
            "success": False,
            "message": str(ex),
            "data": None,
        }


# ==========================================================
# Save PowerShell Script
# ==========================================================

def save_powershell_script(
    filename: str,
    script: str,
) -> dict[str, Any]:
    """
    Save generated PowerShell script.
    """

    try:

        #script_dir = Path("scripts/powershell")
        script_dir = Path(settings.script_output_dir)

        script_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        script_path = script_dir / filename

        script_path.write_text(
            script,
            encoding="utf-8",
        )

        app_logger.success(f"Script saved -> {script_path}")

        return {
            "success": True,
            "message": "PowerShell script saved.",
            "data": str(script_path),
        }

    except Exception as ex:

        app_logger.exception(ex)

        return {
            "success": False,
            "message": str(ex),
            "data": None,
        }


# ==========================================================
# Health Check Tool
# ==========================================================

def health_check() -> dict[str, Any]:
    """
    Returns application health.
    """

    return {
        "success": True,
        "message": "Application is healthy.",
        "data": {
            "parser": "OK",
            "sanitizer": "OK",
            "reports": "OK",
            "scripts": "OK",
        },
    }


# ==========================================================
# Tool Registry
# ==========================================================

ADK_TOOLS = [
    parse_backup_log,
    sanitize_backup_log,
    save_incident_report,
    save_powershell_script,
    health_check,
]