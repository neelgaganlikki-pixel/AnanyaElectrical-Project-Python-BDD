import pytest
from playwright.sync_api import Page, expect
from pages.contact_page import ContactPage

@pytest.mark.negative
@pytest.mark.regression
def test_empty_form_submission_html5_validation(page: Page, contact_page: ContactPage, base_url: str):
    """TC_NEG_001: Verify form submission is blocked by HTML5 required validation when inputs are empty."""
    contact_page.navigate_to(base_url)
    contact_page.scroll_to_element("#quote-form")
    
    # Click submit directly
    contact_page.submit_form()
    
    # Assert form is not submitted and name field is invalid
    validity = page.evaluate("() => document.getElementById('client-name').checkValidity()")
    assert validity is False, "Expected client-name to be invalid on empty submit"

@pytest.mark.negative
@pytest.mark.regression
def test_invalid_phone_number_rejected(page: Page, contact_page: ContactPage, base_url: str):
    """TC_NEG_002: Verify submission is rejected with validation alert when invalid phone number is entered."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="Test Client",
        phone="12345",  # Invalid format
        location="Bengaluru",
        confirm_compliance=True
    )
    contact_page.submit_form()
    page.wait_for_timeout(500)
    
    err_msg = contact_page.get_error_message()
    assert err_msg is not None, "Expected validation alert error message"
    assert "10-digit Indian mobile number" in err_msg

@pytest.mark.negative
@pytest.mark.regression
def test_invalid_email_format_rejected(page: Page, contact_page: ContactPage, base_url: str):
    """TC_NEG_003: Verify submission is rejected when invalid email format is entered."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="Test Client",
        phone="+91 97434 61955",
        location="Bengaluru",
        email="test@invalid",  # Passes HTML5 simple check, but triggers custom React regex requiring valid domain
        confirm_compliance=True
    )
    contact_page.submit_form()
    page.wait_for_timeout(500)
    
    err_msg = contact_page.get_error_message()
    assert err_msg is not None, "Expected validation alert error message"
    assert "valid official email address" in err_msg

@pytest.mark.negative
@pytest.mark.regression
def test_unchecked_compliance_blocked(page: Page, contact_page: ContactPage, base_url: str):
    """TC_NEG_004: Verify submission is blocked when compliance checkbox is unchecked."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="Test Client",
        phone="+91 97434 61955",
        location="Bengaluru",
        confirm_compliance=False  # Explicitly unchecks pre-checked checkbox
    )
    contact_page.submit_form()
    
    validity = page.evaluate("() => document.getElementById('compliance-check').checkValidity()")
    assert validity is False, "Expected compliance-check checkbox to require checking"

# Boundary Value Analysis
@pytest.mark.negative
@pytest.mark.regression
def test_phone_boundary_9_digits_rejected(page: Page, contact_page: ContactPage, base_url: str):
    """TC_BVA_001: Verify phone number with 9 digits (Min - 1) is rejected."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="BVA Client",
        phone="987654321",  # 9 digits
        location="Peenya",
        confirm_compliance=True
    )
    contact_page.submit_form()
    page.wait_for_timeout(500)
    err = contact_page.get_error_message()
    assert err and "10-digit" in err

@pytest.mark.negative
@pytest.mark.regression
def test_phone_boundary_11_digits_rejected(page: Page, contact_page: ContactPage, base_url: str):
    """TC_BVA_003: Verify phone number with 11 digits without country code (Max + 1) is rejected."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="BVA Client",
        phone="98765432109",  # 11 digits
        location="Peenya",
        confirm_compliance=True
    )
    contact_page.submit_form()
    page.wait_for_timeout(500)
    err = contact_page.get_error_message()
    assert err and "10-digit" in err

# Positive Testing
@pytest.mark.positive
@pytest.mark.smoke
@pytest.mark.regression
def test_valid_quote_form_submission(page: Page, contact_page: ContactPage, base_url: str):
    """TC_POS_001: Verify successful quote request submission with valid fields displays confirmation."""
    contact_page.navigate_to(base_url)
    contact_page.fill_consultation_form(
        name="Precision Industrial Automation Ltd.",
        phone="+91 97434 61955",
        category="substation",
        location="Peenya Industrial Area Phase 1",
        email="projects@precision-automation.com",
        notes="500 kVA Transformer and HT Switchgear panel audit.",
        confirm_compliance=True,
        preferred_channel="whatsapp"
    )
    contact_page.submit_form()
    page.wait_for_timeout(800)
    
    assert contact_page.is_confirmation_displayed(), "Confirmation banner was not displayed"
    conf_text = contact_page.get_confirmation_text()
    assert "Inquiry Logged (AES-HOM-" in conf_text

@pytest.mark.positive
@pytest.mark.regression
def test_preferred_response_channel_toggle(page: Page, contact_page: ContactPage, base_url: str):
    """TC_POS_003: Verify Preferred Instant Response Channel toggles between WhatsApp and Email."""
    contact_page.navigate_to(base_url)
    contact_page.scroll_to_element("#quote-form")
    
    wa_btn = page.locator("#quote-form button:has-text('WhatsApp')")
    email_btn = page.locator("#quote-form button:has-text('Email')")
    
    wa_btn.click()
    page.wait_for_timeout(200)
    assert "bg-[#25D366]" in (wa_btn.get_attribute("class") or "")
    
    email_btn.click()
    page.wait_for_timeout(200)
    assert "bg-[#0284C7]" in (email_btn.get_attribute("class") or "")
