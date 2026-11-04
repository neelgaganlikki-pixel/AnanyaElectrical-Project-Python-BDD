import os
import json
from typing import Dict, Any, Optional

class JiraIntegration:
    """Enterprise Jira REST API client for logging validated application defects."""

    def __init__(self):
        self.jira_url = os.environ.get("JIRA_BASE_URL")
        self.jira_user = os.environ.get("JIRA_USER_EMAIL")
        self.jira_token = os.environ.get("JIRA_API_TOKEN")
        self.jira_project_key = os.environ.get("JIRA_PROJECT_KEY", "AES")
        self.auto_create_enabled = os.environ.get("JIRA_AUTO_CREATE", "false").lower() == "true"
        self._tracked_defects = set()

    def create_defect_payload(
        self,
        test_case_id: str,
        summary: str,
        environment: str,
        severity: str,
        priority: str,
        reproduction_steps: str,
        expected_result: str,
        actual_result: str,
        screenshot_path: Optional[str] = None,
        logs: Optional[str] = None
    ) -> Dict[str, Any]:
        return {
            "project_key": self.jira_project_key,
            "test_case_id": test_case_id,
            "summary": f"[{environment.upper()}] {summary}",
            "severity": severity,
            "priority": priority,
            "environment": environment,
            "description": (
                f"*Test Case ID:* {test_case_id}\n"
                f"*Environment:* {environment}\n\n"
                f"*Reproduction Steps:*\n{reproduction_steps}\n\n"
                f"*Expected Result:*\n{expected_result}\n\n"
                f"*Actual Result:*\n{actual_result}\n\n"
                f"*Attached Screenshot:* {screenshot_path or 'N/A'}\n"
            ),
            "execution_logs": logs or "",
            "status": "DRAFT_READY"
        }

    def dispatch_defect(self, defect_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches defect if Jira API is configured and approved, else queues safely as validated defect report."""
        test_id = defect_payload.get("test_case_id")
        if test_id in self._tracked_defects:
            return {"status": "SKIPPED", "reason": f"Duplicate defect suppressed for {test_id}"}

        self._tracked_defects.add(test_id)

        if not (self.jira_url and self.jira_token and self.auto_create_enabled):
            # Save local defect dossier
            dossier_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "defects")
            os.makedirs(dossier_dir, exist_ok=True)
            dossier_file = os.path.join(dossier_dir, f"jira_ready_{test_id}.json")
            with open(dossier_file, "w", encoding="utf-8") as f:
                json.dump(defect_payload, f, indent=2)
            return {
                "status": "QUEUED_LOCALLY",
                "message": f"Jira integration is in dry-run/readiness mode. Defect dossier prepared: {dossier_file}"
            }

        # If live Jira API is configured and approved:
        try:
            import requests
            url = f"{self.jira_url.rstrip('/')}/rest/api/2/issue"
            auth = (self.jira_user, self.jira_token)
            headers = {"Content-Type": "application/json"}
            issue_data = {
                "fields": {
                    "project": {"key": self.jira_project_key},
                    "summary": defect_payload["summary"],
                    "description": defect_payload["description"],
                    "issuetype": {"name": "Bug"},
                    "priority": {"name": defect_payload["priority"]}
                }
            }
            res = requests.post(url, auth=auth, headers=headers, json=issue_data, timeout=10)
            if res.status_code == 201:
                return {"status": "CREATED", "issue_key": res.json().get("key")}
            else:
                return {"status": "FAILED", "code": res.status_code, "error": res.text}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

