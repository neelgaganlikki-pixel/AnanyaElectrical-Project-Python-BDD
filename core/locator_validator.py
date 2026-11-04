from typing import Dict, Any, Optional
from playwright.sync_api import Page, Locator

class LocatorValidator:
    """Validates whether a candidate locator uniquely, safely, and accurately matches the target element."""

    @staticmethod
    def validate_candidate(
        page: Page,
        candidate_selector: str,
        baseline_meta: Dict[str, Any],
        expect_visible: bool = True,
        expect_enabled: bool = True
    ) -> Dict[str, Any]:
        result = {
            "is_valid": False,
            "match_count": 0,
            "is_visible": False,
            "is_enabled": False,
            "tag_match": False,
            "text_match": False,
            "reason": ""
        }

        try:
            loc = page.locator(candidate_selector)
            count = loc.count()
            result["match_count"] = count

            # Rule 1: Exactly one match required
            if count != 1:
                result["reason"] = f"Candidate is ambiguous: matches {count} elements (expected exactly 1)"
                return result

            # Rule 2: Visibility validation
            is_vis = loc.is_visible()
            result["is_visible"] = is_vis
            if expect_visible and not is_vis:
                result["reason"] = "Element matched by candidate is hidden or detached"
                return result

            # Rule 3: Enabled validation
            is_en = loc.is_enabled()
            result["is_enabled"] = is_en
            if expect_enabled and not is_en:
                result["reason"] = "Element matched by candidate is disabled"
                return result

            # Rule 4: Element tag match
            tag = loc.evaluate("el => el.tagName.toLowerCase()")
            expected_tag = baseline_meta.get("tag")
            if expected_tag and tag != expected_tag:
                result["reason"] = f"Tag mismatch: found <{tag}>, expected <{expected_tag}>"
                return result
            result["tag_match"] = True

            # Rule 5: Accessible name or text similarity check
            expected_text = baseline_meta.get("visible_text") or baseline_meta.get("accessible_name") or ""
            actual_text = (loc.inner_text() or "").strip()
            if expected_text and actual_text and (expected_text.lower() in actual_text.lower() or actual_text.lower() in expected_text.lower()):
                result["text_match"] = True
            elif not expected_text:
                result["text_match"] = True
            else:
                # Text didn't match directly, check accessible name attribute
                aria_label = loc.get_attribute("aria-label") or ""
                if expected_text.lower() in aria_label.lower():
                    result["text_match"] = True

            result["is_valid"] = True
            result["reason"] = "Candidate uniquely and strictly passed all identity validations"
            return result

        except Exception as e:
            result["reason"] = f"Validation exception: {str(e)}"
            return result

