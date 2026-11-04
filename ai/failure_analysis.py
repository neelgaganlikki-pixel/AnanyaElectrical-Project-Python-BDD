import os
import json
import datetime
from typing import Dict, Any, Optional
from ai.ai_client import AIClient

class FailureAnalyzer:
    """Orchestrates comprehensive test failure analysis, saving reports to reports/defects/."""

    def __init__(self):
        self.client = AIClient()

    def analyze_failure(
        self,
        test_name: str,
        environment: str,
        base_url: str,
        exception: Exception,
        locator: Optional[str] = None,
        console_errors: Optional[list] = None,
        network_errors: Optional[list] = None,
        screenshot_path: Optional[str] = None,
        dom_snippet: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "test_name": test_name,
            "environment": environment,
            "base_url": base_url,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "locator": locator,
            "console_errors": console_errors or [],
            "network_errors": network_errors or [],
            "dom_snippet": dom_snippet or "",
            "screenshot_path": screenshot_path,
            "timestamp": datetime.datetime.now().isoformat()
        }

        analysis = self.client.analyze(payload)
        full_report = {
            **payload,
            "ai_analysis": analysis
        }

        # Save to reports/defects
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "defects")
        os.makedirs(reports_dir, exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in test_name)
        report_file = os.path.join(reports_dir, f"defect_{safe_name}.json")

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(full_report, f, indent=2)

        return full_report

