"""
Incident Analysis Agent

Analyzes a sanitized backup log and produces a structured
Incident using Gemini.

Author: Mahesh Kolekar
Project: Backup Failure Triage Agent
"""

from __future__ import annotations

from config import settings
from core import generate_incident_id, prompt_loader, response_parser, AgentExecutionError
from models.incident import Incident
from services import app_logger, gemini_service
from tools.log_parser import log_parser
from tools.sanitizer import log_sanitizer


class IncidentAnalysisAgent:
    """
    Turns a raw backup log into a structured Incident.
    """

    def analyze(self, log_path: str) -> Incident:
        """
        Parse, sanitize, and analyze a backup log file.
        """

        app_logger.info(f"Incident Analysis Agent -> Starting analysis of {log_path}")

        parsed = log_parser.parse_file(log_path)

        log_text = parsed["raw_log"]

        if settings.enable_log_sanitization:
            log_text = log_sanitizer.sanitize(log_text)

        prompt = prompt_loader.render(
            "incident_prompt",
            log=log_text,
            job_name=parsed.get("job_name") or "Unknown",
            vm_name=parsed.get("vm_name") or "Unknown",
            repository=parsed.get("repository") or "Unknown",
            error_code=parsed.get("error_code") or "Unknown",
        )

        try:
            raw_response = gemini_service.generate(prompt)
        except Exception as ex:
            app_logger.exception("Incident Analysis Agent failed to call Gemini.")
            raise AgentExecutionError(str(ex)) from ex

        incident_data = response_parser.extract_json(
            response_parser.clean_response(raw_response)
        )

        # Fields we already know from regex parsing / generation,
        # rather than trusting the LLM to invent them.
        incident_data.setdefault("incident_id", generate_incident_id())
        incident_data.setdefault("backup_job", parsed.get("job_name") or "Unknown")
        incident_data.setdefault("vm_name", parsed.get("vm_name"))
        incident_data.setdefault("repository", parsed.get("repository"))
        incident_data.setdefault("error_code", parsed.get("error_code"))
        incident_data.setdefault("raw_log", parsed.get("raw_log"))

        incident = response_parser.validate(incident_data, Incident)

        app_logger.success(
            f"Incident {incident.incident_id} analyzed. "
            f"Root cause: {incident.root_cause}"
        )

        return incident


# Singleton
incident_analysis_agent = IncidentAnalysisAgent()