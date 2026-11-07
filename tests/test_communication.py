import urllib.parse
import pytest
from playwright.sync_api import Page
from pages.navigation_page import NavigationPage

@pytest.mark.integration
@pytest.mark.production_safe
def test_emergency_grid_hotline_dialer(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_COMM_001: Verify 24/7 Grid Emergency Hotline link targets tel:+918660121438."""
    nav_page.navigate_to(base_url)
    
    emergency_links = page.locator("a[href='tel:+918660121438']")
    count = emergency_links.count()
    assert count >= 1, "Expected at least one dedicated 24/7 Emergency Hotline dialer link"
    
    # Verify link text or nearby text mentions Emergency
    text_content = emergency_links.first.inner_text()
    assert "8660121438" in text_content or "Emergency" in text_content

@pytest.mark.integration
@pytest.mark.production_safe
def test_primary_business_telephone_dialer(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_COMM_002: Verify primary business desk phone links target tel:+919632025123."""
    nav_page.navigate_to(base_url)
    
    primary_links = page.locator("a[href='tel:+919632025123']")
    count = primary_links.count()
    assert count >= 1, "Expected primary telephone links pointing to +91 9632025123"
    
    # Inspect visible formatted text
    has_formatted = any("9632025123" in primary_links.nth(i).inner_text() for i in range(count))
    assert has_formatted, "Primary telephone number should be displayed clearly to users"

@pytest.mark.integration
@pytest.mark.production_safe
def test_whatsapp_precomposed_payload(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_COMM_003: Verify WhatsApp click-to-chat URL targets 919632025123 with sanitized precomposed text."""
    nav_page.navigate_to(base_url)
    
    wa_links = page.locator("a[href*='wa.me'], a[href*='whatsapp.com']")
    assert wa_links.count() >= 1, "WhatsApp CTA link not found"
    
    wa_href = wa_links.first.get_attribute("href")
    assert "919632025123" in wa_href, f"WhatsApp target should be 919632025123, got: {wa_href}"
    
    # Parse query parameters
    parsed = urllib.parse.urlparse(wa_href)
    params = urllib.parse.parse_qs(parsed.query)
    assert "text" in params, "WhatsApp link missing precomposed greeting text parameter"
    
    greeting = params["text"][0]
    assert "Ananya Electrical Solutions" in greeting
    assert "electrical contracting" in greeting or "solar installation" in greeting

@pytest.mark.security
@pytest.mark.production_safe
def test_instagram_profile_security_link(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_COMM_004: Verify official Instagram link targets company profile with rel='noopener noreferrer'."""
    nav_page.navigate_to(base_url)
    
    insta_link = page.locator("a[href*='instagram.com/ananyaelectricalsolutions']").first
    assert insta_link.is_visible(), "Instagram profile link not visible in page footer"
    
    target = insta_link.get_attribute("target")
    rel = insta_link.get_attribute("rel")
    
    assert target == "_blank", "Instagram link should open in a new tab"
    assert rel is not None and "noopener" in rel and "noreferrer" in rel, "Insecure external link: missing rel='noopener noreferrer'"

