"""
Remediation Agent

Generates a safe remediation plan (and optional scripts)
for an analyzed Incident.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from core import prompt_loader, response_parser, AgentExecutionError
from models.incident import Incident
from models.remediation import Remediation
from services import app_logger, gemini_service


class RemediationAgent:
    """
    Turns an Incident into a Remediation plan.
    """

    def remediate(self, incident: Incident) -> Remediation:
        """
        Generate a remediation plan for the given incident.
        """

        app_logger.info(
            f"Remediation Agent -> Building plan for {incident.incident_id}"
        )

        prompt = prompt_loader.render(
            "remediation_prompt",
            incident_json=incident.model_dump_json(indent=2),
        )

        try:
            raw_response = gemini_service.generate(prompt)
        except Exception as ex:
            app_logger.exception("Remediation Agent failed to call Gemini.")
            raise AgentExecutionError(str(ex)) from ex

        remediation_data = response_parser.extract_json(
            response_parser.clean_response(raw_response)
        )

        remediation_data.setdefault("incident_id", incident.incident_id)
        remediation_data.setdefault("root_cause", incident.root_cause)

        remediation = response_parser.validate(remediation_data, Remediation)

        app_logger.success(
            f"Remediation plan ready for {incident.incident_id} "
            f"(risk: {remediation.risk_level})"
        )

        return remediation


# Singleton
remediation_agent = RemediationAgent()