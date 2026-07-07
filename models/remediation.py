"""
Remediation Model

Defines the structured output produced by the
Remediation Agent.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class RemediationStep(BaseModel):
    """
    Individual remediation step.
    """

    step_number: int = Field(
        ...,
        description="Execution order."
    )

    description: str = Field(
        ...,
        description="Description of the remediation step."
    )


class RemediationScript(BaseModel):
    """
    Generated remediation script.
    """

    script_type: str = Field(
        ...,
        description="powershell or bash"
    )

    filename: str = Field(
        ...,
        description="Suggested script filename."
    )

    content: str = Field(
        ...,
        description="Script contents."
    )


class Remediation(BaseModel):
    """
    AI generated remediation plan.
    """

    incident_id: str = Field(
        ...,
        description="Related incident ID."
    )

    root_cause: str = Field(
        ...,
        description="Detected root cause."
    )

    recommendation: str = Field(
        ...,
        description="Primary recommendation."
    )

    estimated_downtime: str = Field(
        default="Unknown",
        description="Estimated downtime."
    )

    risk_level: str = Field(
        default="Medium",
        description="Low, Medium, High, Critical."
    )

    requires_human_approval: bool = Field(
        default=False,
        description="Whether engineer approval is required."
    )

    engineer_checklist: List[RemediationStep] = Field(
        default_factory=list,
        description="Recommended execution steps."
    )

    powershell_script: Optional[RemediationScript] = Field(
        default=None,
        description="Generated PowerShell script."
    )

    bash_script: Optional[RemediationScript] = Field(
        default=None,
        description="Generated Bash script."
    )

    notes: Optional[str] = Field(
        default=None,
        description="Additional implementation notes."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "incident_id": "INC-20260703-001",
                "root_cause": "Backup repository is full.",
                "recommendation": "Expand repository capacity and retry the backup.",
                "estimated_downtime": "10 minutes",
                "risk_level": "High",
                "requires_human_approval": False,
                "engineer_checklist": [
                    {
                        "step_number": 1,
                        "description": "Verify repository free space."
                    },
                    {
                        "step_number": 2,
                        "description": "Expand storage volume."
                    },
                    {
                        "step_number": 3,
                        "description": "Restart backup service if required."
                    },
                    {
                        "step_number": 4,
                        "description": "Retry failed backup job."
                    }
                ],
                "powershell_script": {
                    "script_type": "powershell",
                    "filename": "expand_repository.ps1",
                    "content": "Write-Host 'Repository validation placeholder'"
                },
                "bash_script": None,
                "notes": "Verify storage health before rerunning production backups."
            }
        }