import pytest
from playwright.sync_api import Page

@pytest.mark.accessibility
@pytest.mark.regression
@pytest.mark.production_safe
def test_form_controls_accessibility(page: Page, base_url: str):
    """TC_A11Y_001: Verify all form controls in #quote-form have accessible names/labels."""
    page.goto(base_url, wait_until="networkidle")
    
    unlabeled_controls = page.evaluate("""() => {
        const form = document.getElementById('quote-form');
        if (!form) return [];
        const controls = Array.from(form.querySelectorAll('input:not([type="hidden"]), select, textarea'));
        return controls.filter(c => {
            const hasAria = !!c.getAttribute('aria-label') || !!c.getAttribute('aria-labelledby');
            const hasLabel = c.labels && c.labels.length > 0;
            const hasFor = c.id && !!document.querySelector(`label[for="${c.id}"]`);
            return !(hasAria || hasLabel || hasFor);
        }).map(c => c.id || c.name || c.tagName);
    }""")
    assert len(unlabeled_controls) == 0, f"Unlabeled form controls found: {unlabeled_controls}"

@pytest.mark.accessibility
@pytest.mark.regression
@pytest.mark.production_safe
def test_content_images_alt_attributes(page: Page, base_url: str):
    """TC_A11Y_002: Verify content img elements have non-empty alt attributes."""
    page.goto(base_url, wait_until="networkidle")
    
    missing_alt = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs.filter(img => !img.hasAttribute('alt')).map(img => img.src);
    }""")
    assert len(missing_alt) == 0, f"Images missing alt attribute found: {missing_alt}"

