import os
import time
import datetime
from typing import Dict, Any, List, Optional, Callable
from playwright.sync_api import Page, Locator
from core.locator_engine import LocatorEngine
from core.locator_validator import LocatorValidator
from core.healing_history import HealingHistory

class SelfHealingEngine:
    """Enterprise-grade self-healing locator engine with scoring, validation, and strict safety rules."""

    def __init__(self, mode: str = "ASSISTED", confidence_threshold: int = 50):
        self.mode = mode.upper()  # STRICT, ASSISTED, AUTO
        self.confidence_threshold = confidence_threshold
        self.locator_engine = LocatorEngine()
        self.history = HealingHistory()
        self.validator = LocatorValidator()

    def set_mode(self, mode: str):
        self.mode = mode.upper()

    def resolve_and_execute(
        self,
        page: Page,
        element_key: str,
        action: str,
        action_arg: Optional[str] = None,
        timeout_ms: int = 8000
    ) -> Any:
        meta = self.locator_engine.get_element_meta(element_key)
        if not meta:
            raise KeyError(f"Element '{element_key}' is not registered in baseline locators.")

        primary_locator_str = meta.get("original_locator")
        
        # 1. Attempt Primary Locator
        try:
            loc = page.locator(primary_locator_str)
            loc.wait_for(state="visible", timeout=timeout_ms)
            return self._perform_action(loc, action, action_arg)
        except Exception as primary_error:
            # 2. Check execution mode
            if self.mode == "STRICT":
                self._record_failure(element_key, meta, primary_locator_str, str(primary_error), None, "STRICT_MODE_NO_HEAL")
                raise primary_error

            # 3. Discovery & Scoring of Candidates
            candidates = self._discover_and_score_candidates(page, meta)
            
            # Filter candidates matching threshold
            valid_candidates = [c for c in candidates if c["score"] >= self.confidence_threshold]

            if not valid_candidates:
                self._record_failure(element_key, meta, primary_locator_str, str(primary_error), candidates, "NO_QUALIFIED_CANDIDATES")
                raise primary_error

            best_candidate = valid_candidates[0]
            candidate_selector = best_candidate["selector"]

            # 4. Strict Validation of the Candidate
            val_result = self.validator.validate_candidate(
                page=page,
                candidate_selector=candidate_selector,
                baseline_meta=meta
            )

            if not val_result["is_valid"]:
                self._record_failure(
                    element_key, meta, primary_locator_str, str(primary_error), candidates, 
                    f"VALIDATION_FAILED: {val_result['reason']}"
                )
                raise primary_error

            # 5. In ASSISTED or AUTO mode, set approval
            human_status = "APPROVED" if self.mode == "AUTO" else "SUGGESTED"

            # 6. Attempt Controlled Recovery
            try:
                recovered_loc = page.locator(candidate_selector)
                result = self._perform_action(recovered_loc, action, action_arg)

                # Record Success
                self._record_event(
                    element_key=element_key,
                    meta=meta,
                    original_selector=primary_locator_str,
                    original_error=str(primary_error),
                    candidates=candidates,
                    chosen_candidate=best_candidate,
                    validation_result=val_result,
                    recovery_result="SUCCESS",
                    human_status=human_status
                )
                return result

            except Exception as recovery_error:
                self._record_failure(
                    element_key, meta, primary_locator_str, str(primary_error), candidates,
                    f"ACTION_RECOVERY_FAILED: {str(recovery_error)}"
                )
                raise recovery_error

    def _discover_and_score_candidates(self, page: Page, meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        candidates = []
        tag = meta.get("tag", "")
        role = meta.get("role")
        acc_name = meta.get("accessible_name")
        elem_id = meta.get("id")
        placeholder = meta.get("placeholder")
        text = meta.get("visible_text")
        parent = meta.get("parent_context", "")

        # Composite Candidate 1: Parent context + Tag + Text + Accessible Role & Name
        # Scoring: Role/Name (25) + Text (10) + Parent Context (10) + Tag Match (10) = 55 points
        if text and tag:
            sel = f"{parent} {tag}:has-text('{text}')" if parent else f"{tag}:has-text('{text}')"
            score = 25 + 10 + (10 if parent else 0) + (10 if role else 0)
            candidates.append({"selector": sel, "score": score, "reason": "Parent context + tag + text + role composite"})

        # Candidate 2: Accessible role + name
        if role and acc_name:
            sel = f"{parent} [role='{role}']:has-text('{acc_name}')" if parent else f"[role='{role}']:has-text('{acc_name}')"
            score = 25 + (10 if parent else 0)
            candidates.append({"selector": sel, "score": score, "reason": "Accessible role and name match"})

        # Candidate 3: Tag + Placeholder
        if placeholder:
            sel = f"{parent} {tag}[placeholder='{placeholder}']" if parent else f"{tag}[placeholder='{placeholder}']"
            score = 15 + 10 + (10 if parent else 0)
            candidates.append({"selector": sel, "score": score, "reason": "Placeholder + tag match"})

        # Candidate 4: ID with Parent Context
        if elem_id and parent:
            sel = f"{parent} #{elem_id}"
            candidates.append({"selector": sel, "score": 30, "reason": "Parent context + ID match"})
        elif elem_id:
            candidates.append({"selector": f"#{elem_id}", "score": 20, "reason": "Unique ID match"})

        # Sort candidates descending by score
        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates

    def _perform_action(self, locator: Locator, action: str, action_arg: Optional[str] = None) -> Any:
        if action == "click":
            return locator.click()
        elif action == "fill":
            return locator.fill(action_arg or "")
        elif action == "get_text":
            return locator.inner_text()
        elif action == "is_visible":
            return locator.is_visible()
        elif action == "check":
            return locator.check()
        elif action == "select_option":
            return locator.select_option(action_arg or "")
        else:
            raise ValueError(f"Unsupported action: '{action}'")

    def _record_event(self, element_key, meta, original_selector, original_error, candidates, chosen_candidate, validation_result, recovery_result, human_status):
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "element_key": element_key,
            "page": meta.get("page", "unknown"),
            "original_locator": original_selector,
            "original_error": original_error[:300],
            "chosen_candidate": chosen_candidate,
            "candidate_score": chosen_candidate.get("score") if chosen_candidate else 0,
            "candidates": candidates,
            "validation_result": validation_result,
            "recovery_result": recovery_result,
            "human_approval_status": human_status
        }
        self.history.record_healing_event(event)

    def _record_failure(self, element_key, meta, original_selector, error_msg, candidates, reason):
        event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "element_key": element_key,
            "page": meta.get("page", "unknown"),
            "original_locator": original_selector,
            "original_error": error_msg[:300],
            "chosen_candidate": None,
            "candidate_score": 0,
            "candidates": candidates or [],
            "validation_result": {"is_valid": False, "reason": reason},
            "recovery_result": "FAILED",
            "human_approval_status": "REJECTED"
        }
        self.history.record_healing_event(event)
