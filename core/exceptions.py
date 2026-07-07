"""
Application Exceptions

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""


class BackupTriageError(Exception):
    """
    Base exception for the application.
    """

    pass


class PromptNotFoundError(BackupTriageError):
    """
    Raised when a prompt file cannot be found.
    """

    pass


class AgentExecutionError(BackupTriageError):
    """
    Raised when an AI Agent fails.
    """

    pass


class ReportGenerationError(BackupTriageError):
    """
    Raised when report generation fails.
    """

    pass


class ScriptGenerationError(BackupTriageError):
    """
    Raised when PowerShell generation fails.
    """

    pass


class InvalidLogError(BackupTriageError):
    """
    Raised when the uploaded log cannot be parsed.
    """

    pass