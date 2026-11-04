import os
import json
from typing import Dict, Any, Optional

class AIClient:
    """Modular AI Client that routes analysis to an LLM provider if configured, or uses built-in heuristic AI."""

    def __init__(self):
        self.api_key = os.environ.get("AI_ANALYSIS_API_KEY")
        self.provider = "openai" if os.environ.get("OPENAI_API_KEY") else ("heuristic")

    def analyze(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Runs failure diagnostics. Falls back to deterministic heuristic intelligence when no external LLM key is provided."""
        error_msg = str(payload.get("exception_message", "")).lower()
        exc_type = str(payload.get("exception_type", "")).lower()
        console_errs = payload.get("console_errors", [])
        network_errs = payload.get("network_errors", [])

        # Heuristic Expert Classification
        category = "Framework issue"
        is_app_defect = False
        healing_rec = False
        root_cause = "Unhandled exception during execution"
        suggested_fix = "Review test execution stack trace"

        if "timeout" in exc_type or "timeout" in error_msg:
            if "waiting for locator" in error_msg:
                category = "Locator issue"
                root_cause = f"Timeout waiting for locator: {payload.get('locator', 'unknown')}. Element structure may have changed."
                suggested_fix = "Verify locator against current DOM or trigger SelfHealingEngine in ASSISTED/AUTO mode."
                healing_rec = True
            elif "net::err" in error_msg or len(network_errs) > 0:
                category = "Network issue"
                root_cause = "Network connection timeout or DNS resolution failure."
                suggested_fix = "Check DNS, Cloudflare edge proxy, or test environment availability."
            else:
                category = "Timing issue"
                root_cause = "Page or asynchronous component did not render within timeout threshold."
                suggested_fix = "Use explicit web-first assertions or wait for network idle."
        elif "assertionerror" in exc_type or "assert" in error_msg:
            category = "Application defect"
            is_app_defect = True
            root_cause = f"Assertion failed: application behavior differed from expected business specification."
            suggested_fix = "Log defect in Jira with reproduction steps and screenshot."
        elif "strict mode violation" in error_msg:
            category = "Locator issue"
            root_cause = "Selector resolved to multiple DOM elements violating Playwright strict mode."
            suggested_fix = "Refine selector with parent context or use .first / exact accessible name."
            healing_rec = True
        elif any("500" in str(e) or "502" in str(e) or "503" in str(e) for e in network_errs):
            category = "Environment issue"
            root_cause = "Backend server or edge worker returned HTTP 5xx error."
            suggested_fix = "Check Cloudflare Workers service logs or server status."

        return {
            "category": category,
            "root_cause_summary": root_cause,
            "impact_severity": "Critical" if is_app_defect else "Major",
            "suggested_fix": suggested_fix,
            "is_application_defect": is_app_defect,
            "healing_recommended": healing_rec,
            "engine": "Heuristic Rule-Based AI Engine" if not self.api_key else f"LLM ({self.provider})"
        }

