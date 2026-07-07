"""
Application Logger

Provides a centralized logger for the Backup Failure Triage Agent.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from pathlib import Path
import sys

from loguru import logger

from config import settings


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "application.log"


def setup_logger():
    """
    Configure application logging.
    """

    # Remove default logger
    logger.remove()

    # Console Logging
    logger.add(
        sys.stdout,
        level=settings.log_level.upper(),
        colorize=True,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
    )

    # File Logging
    logger.add(
        LOG_FILE,
        level=settings.log_level.upper(),
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        enqueue=True,
        backtrace=True,
        diagnose=True,
        encoding="utf-8",
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        ),
    )

    logger.info("Logger initialized")

    return logger


# Singleton Logger
app_logger = setup_logger()