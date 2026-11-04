import pytest
from playwright.sync_api import Page, expect

@pytest.mark.security
@pytest.mark.regression
@pytest.mark.production_safe
def test_https_enforcement(page: Page, base_url: str):
    """TC_SEC_001: Verify website enforces secure HTTPS protocol."""
    assert base_url.startswith("https://"), f"Base URL {base_url} is not using HTTPS"
    response = page.goto(base_url, wait_until="networkidle")
    assert page.url.startswith("https://")
    assert response.status == 200

@pytest.mark.security
@pytest.mark.regression
@pytest.mark.production_safe
def test_external_link_security_attributes(page: Page, base_url: str):
    """TC_SEC_002: Verify external links with target='_blank' have rel='noopener noreferrer' to prevent reverse tabnabbing."""
    page.goto(base_url, wait_until="networkidle")
    links_without_rel = page.evaluate("""() => {
        const anchors = Array.from(document.querySelectorAll('a[target="_blank"]'));
        return anchors.filter(a => {
            const rel = a.getAttribute('rel') || '';
            return !rel.includes('noopener') && !rel.includes('noreferrer');
        }).map(a => a.href);
    }""")
    assert len(links_without_rel) == 0, f"Found insecure target='_blank' links: {links_without_rel}"

@pytest.mark.security
@pytest.mark.regression
def test_input_xss_sanitization(page: Page, base_url: str):
    """TC_SEC_003: Verify harmless XSS payload string is properly escaped and not executed in DOM."""
    dialog_triggered = []
    page.on("dialog", lambda d: dialog_triggered.append(d.message))
    
    page.goto(base_url, wait_until="networkidle")
    
    # Enter script tag in client-name
    payload = "<script>alert('XSS')</script>"
    page.locator("#client-name").fill(payload)
    page.wait_for_timeout(300)
    
    # Check that no alert was triggered
    assert len(dialog_triggered) == 0, "XSS script payload was executed!"

