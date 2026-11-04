import os
import json
from typing import Dict, Any

class TestDataLoader:
    """Helper to retrieve structured test data and fixtures."""

    @staticmethod
    def load_data(file_path: str = None) -> Dict[str, Any]:
        if not file_path:
            file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_data", "test_data.json")
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

