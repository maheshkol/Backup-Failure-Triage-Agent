"""
Application Settings

Loads configuration from the .env file using Pydantic Settings.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================================================
    # Application
    # ==========================================================

    app_name: str = Field(
        default="Backup Failure Triage Agent",
        alias="APP_NAME",
    )

    app_version: str = Field(
        default="1.0.0",
        alias="APP_VERSION",
    )

    app_env: str = Field(
        default="development",
        alias="APP_ENV",
    )

    log_level: str = Field(
        default="INFO",
        alias="LOG_LEVEL",
    )

    # ==========================================================
    # Gemini
    # ==========================================================

    gemini_api_key: str = Field(
        default="",
        alias="GEMINI_API_KEY",
    )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        alias="GEMINI_MODEL",
    )

    # ==========================================================
    # Database
    # ==========================================================

    database_path: str = Field(
        default="memory/incidents.db",
        alias="DATABASE_PATH",
    )

    # ==========================================================
    # Output
    # ==========================================================

    report_output_dir: str = Field(
        default="output/reports",
        alias="REPORT_OUTPUT_DIR",
    )

    script_output_dir: str = Field(
        default="output/scripts",
        alias="SCRIPT_OUTPUT_DIR",
    )

    sample_log_dir: str = Field(
        default="data/sample_logs",
        alias="SAMPLE_LOG_DIR",
    )

    # ==========================================================
    # MCP
    # ==========================================================

    mcp_host: str = Field(
        default="127.0.0.1",
        alias="MCP_HOST",
    )

    mcp_port: int = Field(
        default=8001,
        alias="MCP_PORT",
    )

    # ==========================================================
    # Security
    # ==========================================================

    enable_log_sanitization: bool = Field(
        default=True,
        alias="ENABLE_LOG_SANITIZATION",
    )

    allow_destructive_commands: bool = Field(
        default=False,
        alias="ALLOW_DESTRUCTIVE_COMMANDS",
    )

    require_human_approval: bool = Field(
        default=True,
        alias="REQUIRE_HUMAN_APPROVAL",
    )

    # ==========================================================
    # AI Confidence
    # ==========================================================

    min_confidence: float = Field(
        default=0.70,
        alias="MIN_CONFIDENCE",
    )

    # ==========================================================
    # CLI
    # ==========================================================

    default_report_format: str = Field(
        default="markdown",
        alias="DEFAULT_REPORT_FORMAT",
    )

    default_script_type: str = Field(
        default="powershell",
        alias="DEFAULT_SCRIPT_TYPE",
    )

    # ==========================================================
    # Future Features
    # ==========================================================

    enable_memory: bool = Field(
        default=True,
        alias="ENABLE_MEMORY",
    )

    enable_vector_search: bool = Field(
        default=False,
        alias="ENABLE_VECTOR_SEARCH",
    )

    enable_pdf_reports: bool = Field(
        default=True,
        alias="ENABLE_PDF_REPORTS",
    )

    enable_json_export: bool = Field(
        default=True,
        alias="ENABLE_JSON_EXPORT",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()


settings = get_settings()