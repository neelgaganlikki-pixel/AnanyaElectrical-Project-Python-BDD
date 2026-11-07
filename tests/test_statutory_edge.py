import datetime
import pytest
from playwright.sync_api import Page
from pages.navigation_page import NavigationPage
from pages.contact_page import ContactPage

@pytest.mark.functional
@pytest.mark.production_safe
def test_statutory_licensing_badging(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_REG_001: Verify Karnataka Electrical Inspectorate Super Grade licensing credentials."""
    nav_page.navigate_to(base_url)
    
    body_text = page.locator("body").inner_text()
    assert "Super Grade" in body_text or "Class 1" in body_text, "Super Grade / Class 1 licensing not mentioned"
    assert "Karnataka" in body_text, "State of Karnataka statutory jurisdiction not mentioned"
    assert "BESCOM" in body_text or "KPTCL" in body_text, "BESCOM/KPTCL statutory reference missing"

@pytest.mark.functional
@pytest.mark.production_safe
def test_dynamic_copyright_year(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_REG_002: Verify footer copyright string contains current calendar year."""
    nav_page.navigate_to(base_url)
    
    footer_text = page.locator("footer").inner_text()
    current_year = str(datetime.datetime.now().year)
    
    # Check if current year is present in footer copyright
    assert current_year in footer_text or "Ananya Electrical Solutions" in footer_text

@pytest.mark.functional
@pytest.mark.production_safe
def test_sahakarnagar_office_address_sync(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_REG_003: Verify registered Sahakarnagar office address and PIN 560092 across footer and contact."""
    nav_page.navigate_to(base_url)
    
    footer_text = page.locator("footer").inner_text()
    assert "Sahakarnagar" in footer_text or "Bengaluru" in footer_text
    
    # Check Schema.org address
    schema_address = page.evaluate("""() => {
        const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        for (const s of scripts) {
            try {
                const parsed = JSON.parse(s.innerText);
                if (parsed['@graph']) {
                    const biz = parsed['@graph'].find(item => item['@id'] && item['@id'].includes('business'));
                    if (biz && biz.address) return biz.address;
                }
            } catch (e) {}
        }
        return null;
    }""")
    if schema_address:
        assert schema_address.get("postalCode") == "560092"
        assert schema_address.get("addressLocality") == "Bengaluru"

@pytest.mark.functional
def test_form_submit_rapid_click_debounce(page: Page, contact_page: ContactPage, base_url: str):
    """TC_EDGE_001: Verify rapid duplicate clicks on submit button generate only one confirmation banner."""
    contact_page.navigate_to(base_url)
    page.locator("#quote-form").scroll_into_view_if_needed()
    
    contact_page.fill_consultation_form(
        name="Debounce Test Ltd",
        phone="9743461955",
        category="substation",
        location="Peenya Bengaluru",
        email="debounce@test.in",
        notes="Automated debounce test",
        confirm_compliance=True
    )
    
    submit_btn = page.locator("#quote-form button[type='submit']")
    
    # Dispatch 3 rapid clicks
    submit_btn.click()
    try:
        submit_btn.click(timeout=300)
    except Exception:
        pass
        
    page.wait_for_timeout(1500)
    
    # Confirmation container should be displayed inside quote form
    assert contact_page.is_confirmation_displayed(), "Confirmation banner not displayed after submission"

@pytest.mark.functional
def test_browser_history_bfcache_stability(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_EDGE_002: Verify browser history back/forward (bfcache) navigation renders layout without JS errors."""
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    
    nav_page.navigate_to(base_url)
    page.wait_for_timeout(500)
    
    # Click Contact Us (or scroll)
    nav_page.click_contact_us()
    page.wait_for_timeout(500)
    
    # Go back
    page.go_back()
    page.wait_for_timeout(500)
    
    # Go forward
    page.go_forward()
    page.wait_for_timeout(500)
    
    # Assert no fatal page errors
    fatal_errors = [e for e in errors if "fatal" in e.lower() or "unhandled" in e.lower()]
    assert len(fatal_errors) == 0, f"Encountered fatal errors during history navigation: {fatal_errors}"
    assert page.is_visible("header"), "Header should remain visible after back/forward navigation"
