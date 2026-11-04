from typing import Dict, Any, List

class LocatorSuggestions:
    """Provides ranked alternative locator suggestions for broken selectors."""

    @staticmethod
    def suggest_alternatives(broken_selector: str, element_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        suggestions = []
        if element_meta.get("accessible_name"):
            suggestions.append({
                "type": "Playwright get_by_label",
                "code": f"page.get_by_label('{element_meta['accessible_name']}')",
                "confidence": "High"
            })
        if element_meta.get("role") and element_meta.get("visible_text"):
            suggestions.append({
                "type": "Playwright get_by_role",
                "code": f"page.get_by_role('{element_meta['role']}', name='{element_meta['visible_text']}')",
                "confidence": "High"
            })
        if element_meta.get("placeholder"):
            suggestions.append({
                "type": "Playwright get_by_placeholder",
                "code": f"page.get_by_placeholder('{element_meta['placeholder']}')",
                "confidence": "Medium"
            })
        if element_meta.get("id"):
            suggestions.append({
                "type": "CSS ID Selector",
                "code": f"#{element_meta['id']}",
                "confidence": "Medium"
            })
        return suggestions

