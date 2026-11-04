import os
import json
import time
from typing import Dict, Any, List

class HealingHistory:
    """Maintains persistent audit trail of locator self-healing actions and suggestions."""
    
    def __init__(self, history_file: str = "locators/healing_history.json", audit_file: str = "locators/healing_audit.json"):
        self.history_file = history_file
        self.audit_file = audit_file
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.history_file):
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)
        if not os.path.exists(self.audit_file):
            with open(self.audit_file, "w", encoding="utf-8") as f:
                json.dump({
                    "summary": {
                        "total_failures": 0,
                        "recovered": 0,
                        "unrecovered": 0,
                        "candidates_generated": 0,
                        "approved_changes": 0,
                        "rejected_changes": 0
                    },
                    "events": []
                }, f, indent=2)

    def record_healing_event(self, event_data: Dict[str, Any]):
        """Records a healing attempt event to both healing_history and healing_audit."""
        # 1. Update history list
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

        history.append(event_data)
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        # 2. Update audit summary
        try:
            with open(self.audit_file, "r", encoding="utf-8") as f:
                audit = json.load(f)
        except Exception:
            audit = {"summary": {}, "events": []}

        summary = audit.setdefault("summary", {
            "total_failures": 0,
            "recovered": 0,
            "unrecovered": 0,
            "candidates_generated": 0,
            "approved_changes": 0,
            "rejected_changes": 0
        })

        summary["total_failures"] = summary.get("total_failures", 0) + 1
        if event_data.get("recovery_result") == "SUCCESS":
            summary["recovered"] = summary.get("recovered", 0) + 1
        else:
            summary["unrecovered"] = summary.get("unrecovered", 0) + 1

        summary["candidates_generated"] = summary.get("candidates_generated", 0) + len(event_data.get("candidates", []))
        
        if event_data.get("human_approval_status") == "APPROVED":
            summary["approved_changes"] = summary.get("approved_changes", 0) + 1
        elif event_data.get("human_approval_status") == "REJECTED":
            summary["rejected_changes"] = summary.get("rejected_changes", 0) + 1

        audit.setdefault("events", []).append(event_data)
        with open(self.audit_file, "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2)

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        try:
            with open(self.audit_file, "r", encoding="utf-8") as f:
                audit = json.load(f)
            summary = audit.get("summary", {})
            total = summary.get("total_failures", 0)
            recovered = summary.get("recovered", 0)
            pct = (recovered / total * 100.0) if total > 0 else 100.0
            return {
                **summary,
                "recovery_percentage": round(pct, 2)
            }
        except Exception:
            return {
                "total_failures": 0,
                "recovered": 0,
                "unrecovered": 0,
                "candidates_generated": 0,
                "approved_changes": 0,
                "rejected_changes": 0,
                "recovery_percentage": 100.0
            }

