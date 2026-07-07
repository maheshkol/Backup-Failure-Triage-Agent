"""
Incident Model

Defines the structured output produced by the
Incident Analysis Agent.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    """
    Supporting evidence found in the backup log.
    """

    description: str = Field(
        ...,
        description="Evidence extracted from the log."
    )


class Incident(BaseModel):
    """
    Represents a backup failure incident.
    """

    incident_id: str = Field(
        ...,
        description="Unique incident identifier."
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Incident creation time."
    )

    backup_job: str = Field(
        ...,
        description="Backup job name."
    )

    vm_name: Optional[str] = Field(
        default=None,
        description="Affected virtual machine."
    )

    repository: Optional[str] = Field(
        default=None,
        description="Backup repository."
    )

    error_code: Optional[str] = Field(
        default=None,
        description="Backup error code."
    )

    root_cause: str = Field(
        ...,
        description="Identified root cause."
    )

    severity: str = Field(
        ...,
        description="Critical, High, Medium or Low."
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="AI confidence score."
    )

    evidence: List[Evidence] = Field(
        default_factory=list,
        description="Evidence supporting the diagnosis."
    )

    recommendation: str = Field(
        ...,
        description="Recommended remediation."
    )

    affected_components: List[str] = Field(
        default_factory=list,
        description="Infrastructure components affected."
    )

    requires_human_approval: bool = Field(
        default=False,
        description="Whether engineer approval is required."
    )

    summary: str = Field(
        ...,
        description="Short incident summary."
    )

    raw_log: Optional[str] = Field(
        default=None,
        description="Original log text."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "INC-20260703-001",
                "backup_job": "Daily_SQL_Backup",
                "vm_name": "SQL01",
                "repository": "Repo01",
                "error_code": "0x00000012",
                "root_cause": "Backup repository is full.",
                "severity": "Critical",
                "confidence": 0.96,
                "recommendation": "Increase repository capacity and retry the backup.",
                "affected_components": [
                    "Repository",
                    "Backup Server"
                ],
                "requires_human_approval": False,
                "summary": "Daily backup failed because the repository has no free space.",
                "evidence": [
                    {
                        "description": "Repository free space reported as 0 GB."
                    },
                    {
                        "description": "Backup session terminated due to insufficient storage."
                    }
                ]
            }
        }