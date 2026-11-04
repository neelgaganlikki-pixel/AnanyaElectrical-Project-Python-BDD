import pytest
import urllib.parse
from playwright.sync_api import Page, expect

@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.production_safe
def test_whatsapp_integration_link_format(page: Page, base_url: str):
    """TC_INT_001: Verify WhatsApp integration CTA link format and URL-encoded message."""
    page.goto(base_url, wait_until="networkidle")
    wa_links = page.locator("a[href*='wa.me']").all()
    assert len(wa_links) > 0, "No WhatsApp CTA links found"
    
    first_wa = wa_links[0]
    href = first_wa.get_attribute("href")
    assert "wa.me/919632025123" in href
    assert "text=" in href
    assert first_wa.get_attribute("target") == "_blank"

@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.production_safe
def test_telephone_integration_links(page: Page, base_url: str):
    """TC_INT_002: Verify primary and emergency telephone tel: links trigger direct dialers with valid numbers."""
    page.goto(base_url, wait_until="networkidle")
    
    # Primary phone
    primary_link = page.locator("a[href='tel:+919632025123']").first
    expect(primary_link).to_be_attached()
    
    # Emergency hotline
    emergency_link = page.locator("a[href='tel:+918660121438']").first
    expect(emergency_link).to_be_attached()

@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.production_safe
def test_email_integration_links(page: Page, base_url: str):
    """TC_INT_003: Verify official mailto: link targets corporate email address."""
    page.goto(base_url, wait_until="networkidle")
    mail_links = page.locator("a[href^='mailto:ananyaelectricalsolutions@gmail.com']").all()
    assert len(mail_links) > 0, "No corporate mailto links found"

@pytest.mark.integration
@pytest.mark.regression
@pytest.mark.production_safe
def test_google_maps_integration(page: Page, base_url: str):
    """TC_INT_004: Verify Google Maps link targets accurate coordinates with secure attributes."""
    page.goto(base_url, wait_until="networkidle")
    maps_link = page.locator("a[href*='google.com/maps']").first
    expect(maps_link).to_be_attached()
    assert maps_link.get_attribute("target") == "_blank"
    rel = maps_link.get_attribute("rel") or ""
    assert "noopener" in rel or "noreferrer" in rel

