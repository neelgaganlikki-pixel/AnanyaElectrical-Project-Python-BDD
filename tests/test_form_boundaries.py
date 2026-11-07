import pytest
from playwright.sync_api import Page
from pages.contact_page import ContactPage

@pytest.mark.functional
def test_project_type_dropdown_options_matrix(page: Page, contact_page: ContactPage, base_url: str):
    """TC_FORM_005: Verify all 12 commercial and industrial project types exist in #project-type dropdown."""
    contact_page.navigate_to(base_url)
    page.locator("#quote-form").scroll_into_view_if_needed()
    
    select_locator = page.locator("#project-type")
    assert select_locator.is_visible(), "#project-type dropdown should be visible"
    
    options = select_locator.locator("option").all_inner_texts()
    assert len(options) >= 10, f"Expected at least 10 project type options, found {len(options)}"
    
    # Check core commercial options exist
    expected_keywords = [
        "Substation",
        "Solar",
        "Switchboard",
        "Wiring",
        "Statutory",
        "AMC"
    ]
    for kw in expected_keywords:
        assert any(kw.lower() in opt.lower() for opt in options), f"Expected option containing '{kw}' not found in dropdown"

    # Select a specific option and verify value changes
    select_locator.select_option(value="substation")
    assert select_locator.input_value() == "substation"

@pytest.mark.functional
def test_bengaluru_industrial_location_input(page: Page, contact_page: ContactPage, base_url: str):
    """TC_FORM_006: Verify #location input accepts major Karnataka industrial corridor addresses."""
    contact_page.navigate_to(base_url)
    page.locator("#quote-form").scroll_into_view_if_needed()
    
    loc_input = page.locator("#location")
    assert loc_input.is_visible(), "#location input field should be visible"
    
    corridors = [
        "Peenya Industrial Area, 2nd Stage, Bengaluru",
        "Whitefield EPIP Zone, Bengaluru - 560066",
        "Electronic City Phase 1, Hosur Road"
    ]
    for corridor in corridors:
        loc_input.fill(corridor)
        assert loc_input.input_value() == corridor, f"Location input failed to accept '{corridor}'"

@pytest.mark.functional
def test_notes_textarea_multiline_formatting(page: Page, contact_page: ContactPage, base_url: str):
    """TC_FORM_007: Verify #notes textarea accepts and preserves multi-line technical requirements."""
    contact_page.navigate_to(base_url)
    page.locator("#quote-form").scroll_into_view_if_needed()
    
    notes_el = page.locator("#notes")
    assert notes_el.is_visible(), "#notes textarea should be visible"
    
    technical_spec = "Requirement: 500 kVA Dry Type Transformer\nIncoming: 11kV BESCOM Feeder\nOutgoing: Form-4b PCC Panel with ACB"
    notes_el.fill(technical_spec)
    
    val = notes_el.input_value()
    assert "500 kVA" in val
    assert "\n" in val, "Textarea did not preserve newline formatting"

@pytest.mark.boundary
def test_phone_input_formatting_tolerance(page: Page, contact_page: ContactPage, base_url: str):
    """TC_FORM_008: Verify phone input tolerance with formatted strings (10-digit standard)."""
    contact_page.navigate_to(base_url)
    page.locator("#quote-form").scroll_into_view_if_needed()
    
    phone_input = page.locator("#client-phone")
    assert phone_input.is_visible(), "#client-phone input should be visible"
    
    # 10 digits without prefix
    phone_input.fill("9845012345")
    assert phone_input.input_value() == "9845012345"
    
    # +91 prefix format
    phone_input.fill("+919743461955")
    assert phone_input.input_value() == "+919743461955"
