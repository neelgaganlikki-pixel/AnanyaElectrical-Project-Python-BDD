import pytest
from playwright.sync_api import Page
from core.self_healing_engine import SelfHealingEngine
from core.locator_engine import LocatorEngine

@pytest.mark.healing
def test_self_healing_successful_recovery(page: Page):
    """TC_HEAL_001: Verify self-healing engine recovers element when primary selector fails but fingerprint matches."""
    # Serve controlled HTML fixture simulating a modified DOM
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <div id="quote-form">
            <button id="renamed-id-v2" type="submit" role="button" aria-label="Submit Engineering Inquiry">
                Submit Engineering Inquiry
            </button>
        </div>
    </body>
    </html>
    """
    page.set_content(html_content)

    engine = SelfHealingEngine(mode="AUTO", confidence_threshold=50)
    
    # Register element with outdated primary selector #legacy-broken-id
    engine.locator_engine.register_element("test.button_recovery", {
        "page": "fixture",
        "element_name": "button_recovery",
        "original_locator": "#legacy-broken-id",  # Broken!
        "tag": "button",
        "id": "renamed-id-v2",
        "role": "button",
        "accessible_name": "Submit Engineering Inquiry",
        "visible_text": "Submit Engineering Inquiry",
        "parent_context": "#quote-form"
    })

    # Execute click via SelfHealingEngine
    # The primary selector #legacy-broken-id will fail, triggering self-healing recovery
    result = engine.resolve_and_execute(
        page=page,
        element_key="test.button_recovery",
        action="is_visible"
    )

    assert result is True, "Self-healing engine failed to recover visible element"

@pytest.mark.healing
def test_self_healing_rejects_missing_element(page: Page):
    """TC_HEAL_002: Verify self-healing engine safely rejects healing when element is genuinely removed."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <div id="content">
            <p>Completely different content</p>
        </div>
    </body>
    </html>
    """
    page.set_content(html_content)

    engine = SelfHealingEngine(mode="AUTO", confidence_threshold=65)
    
    engine.locator_engine.register_element("test.missing_element", {
        "page": "fixture",
        "element_name": "missing_element",
        "original_locator": "#definitely-removed-element",
        "tag": "button",
        "role": "button",
        "accessible_name": "Non-existent Feature",
        "visible_text": "Non-existent Feature"
    })

    with pytest.raises(Exception):
        engine.resolve_and_execute(
            page=page,
            element_key="test.missing_element",
            action="click",
            timeout_ms=1000
        )

@pytest.mark.healing
def test_self_healing_rejects_ambiguous_candidates(page: Page):
    """TC_HEAL_003: Verify self-healing engine rejects candidate when multiple elements match (ambiguity rule)."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <body>
        <div id="container">
            <button class="action-btn">Action 1</button>
            <button class="action-btn">Action 2</button>
        </div>
    </body>
    </html>
    """
    page.set_content(html_content)

    engine = SelfHealingEngine(mode="AUTO", confidence_threshold=10)
    
    # Broken selector targeting ambiguous class without distinction
    engine.locator_engine.register_element("test.ambiguous_element", {
        "page": "fixture",
        "element_name": "ambiguous_element",
        "original_locator": "#broken-action-btn",
        "tag": "button",
        "role": "button",
        "placeholder": None
    })

    with pytest.raises(Exception):
        engine.resolve_and_execute(
            page=page,
            element_key="test.ambiguous_element",
            action="click",
            timeout_ms=1000
        )

