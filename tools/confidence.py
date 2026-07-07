"""
Confidence Utilities

Helpers for evaluating whether an AI-generated Incident
meets the minimum confidence threshold to auto-proceed.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from config import settings
from models.incident import Incident


def meets_threshold(incident: Incident) -> bool:
    """
    Returns True if the incident's confidence score is high
    enough to proceed without mandatory human review.
    """

    return incident.confidence >= settings.min_confidence


def requires_review(incident: Incident) -> bool:
    """
    Returns True if the incident should be flagged for
    human review before remediation.
    """

    if incident.requires_human_approval:
        return True

    if not meets_threshold(incident):
        return True

    if incident.severity in ("Critical", "High"):
        return True

    return False


def confidence_label(incident: Incident) -> str:
    """
    Returns a human-readable confidence label.
    """

    score = incident.confidence

    if score >= 0.85:
        return "High Confidence"

    if score >= settings.min_confidence:
        return "Moderate Confidence"

    return "Low Confidence — Review Recommended"