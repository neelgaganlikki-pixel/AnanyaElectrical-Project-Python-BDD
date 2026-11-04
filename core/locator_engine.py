import os
import json
from typing import Dict, Any, Optional

class LocatorEngine:
    """Manages baseline locator metadata and fingerprints."""
    
    def __init__(self, baseline_path: Optional[str] = None):
        if not baseline_path:
            baseline_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "locators", "baseline_locators.json")
        self.baseline_path = baseline_path
        self._locators = self._load_baseline()

    def _load_baseline(self) -> Dict[str, Any]:
        if os.path.exists(self.baseline_path):
            with open(self.baseline_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_element_meta(self, element_key: str) -> Optional[Dict[str, Any]]:
        return self._locators.get(element_key)

    def register_element(self, element_key: str, meta: Dict[str, Any]):
        self._locators[element_key] = meta
        os.makedirs(os.path.dirname(self.baseline_path), exist_ok=True)
        with open(self.baseline_path, "w", encoding="utf-8") as f:
            json.dump(self._locators, f, indent=2)

