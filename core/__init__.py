"""
Core Framework

Shared framework components used across all AI agents.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from .utils import (
    generate_incident_id,
    generate_report_id,
    generate_script_name,
    load_text_file,
    save_text_file,
    ensure_directory,
    current_timestamp,
    short_uuid,
    timer,
)

from .exceptions import (
    BackupTriageError,
    PromptNotFoundError,
    AgentExecutionError,
    ReportGenerationError,
    ScriptGenerationError,
    InvalidLogError,
)

from .prompt_loader import prompt_loader
from .response_parser import response_parser

__all__ = [
    "generate_incident_id",
    "generate_report_id",
    "generate_script_name",
    "load_text_file",
    "save_text_file",
    "ensure_directory",
    "current_timestamp",
    "short_uuid",
    "timer",
    "BackupTriageError",
    "PromptNotFoundError",
    "AgentExecutionError",
    "ReportGenerationError",
    "ScriptGenerationError",
    "InvalidLogError",
    "prompt_loader",
    "response_parser",
]