"""
Report Agent

Combines an Incident and a Remediation plan into a
polished, MSP-ready incident report.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from core import generate_report_id, prompt_loader, response_parser, AgentExecutionError
from models.incident import Incident
from models.remediation import Remediation
from models.report import Report
from services import app_logger, gemini_service


class ReportAgent:
    """
    Generates the final incident report.
    """

    def generate(self, incident: Incident, remediation: Remediation) -> Report:
        """
        Build a final Report from an Incident and Remediation.
        """

        app_logger.info(
            f"Report Agent -> Drafting report for {incident.incident_id}"
        )

        prompt = prompt_loader.render(
            "report_prompt",
            incident_json=incident.model_dump_json(indent=2),
            remediation_json=remediation.model_dump_json(indent=2),
        )

        try:
            raw_response = gemini_service.generate(prompt)
        except Exception as ex:
            app_logger.exception("Report Agent failed to call Gemini.")
            raise AgentExecutionError(str(ex)) from ex

        report_data = response_parser.extract_json(
            response_parser.clean_response(raw_response)
        )

        report_data.setdefault("report_id", generate_report_id())
        report_data["incident"] = incident.model_dump()
        report_data["remediation"] = remediation.model_dump()

        report = response_parser.validate(report_data, Report)

        app_logger.success(f"Report {report.report_id} generated.")

        return report


# Singleton
report_agent = ReportAgent()