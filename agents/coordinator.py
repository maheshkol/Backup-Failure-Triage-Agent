"""
Coordinator

Orchestrates the full triage pipeline:
Log -> Incident Analysis -> Remediation -> Report -> Save.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from typing import Any

from core import generate_script_name, timer
from models.report import Report
from services import app_logger
from tools.adk_tools import save_incident_report, save_powershell_script
from tools.incident_report import render_markdown_report

from .incident_analysis_agent import incident_analysis_agent
from .remediation_agent import remediation_agent
from .report_agent import report_agent


class Coordinator:
    """
    Runs the end-to-end backup failure triage pipeline.
    """

    @timer
    def run(self, log_path: str) -> dict[str, Any]:
        """
        Run the full pipeline for a single backup log.
        """

        app_logger.info(f"Coordinator -> Starting pipeline for {log_path}")

        incident = incident_analysis_agent.analyze(log_path)
        remediation = remediation_agent.remediate(incident)
        report = report_agent.generate(incident, remediation)

        saved_paths = self._save_artifacts(report)

        app_logger.success(
            f"Coordinator -> Pipeline complete for {incident.incident_id}"
        )

        return {
            "incident": incident,
            "remediation": remediation,
            "report": report,
            "saved_paths": saved_paths,
        }

    # --------------------------------------------------------

    def _save_artifacts(self, report: Report) -> dict[str, str]:
        """
        Save the markdown report and any generated script to disk.
        """

        saved: dict[str, str] = {}

        markdown = render_markdown_report(report)
        report_result = save_incident_report(f"{report.report_id}.md", markdown)

        if report_result["success"]:
            saved["report"] = report_result["data"]

        script = report.remediation.powershell_script

        if script:
            filename = script.filename or generate_script_name("ps1")
            script_result = save_powershell_script(filename, script.content)

            if script_result["success"]:
                saved["powershell_script"] = script_result["data"]

        return saved


# Singleton
coordinator = Coordinator()