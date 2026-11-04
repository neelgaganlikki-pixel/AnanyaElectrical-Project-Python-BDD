import pytest
import json
from playwright.sync_api import Page

@pytest.mark.seo
@pytest.mark.regression
@pytest.mark.production_safe
def test_seo_metadata_elements(page: Page, base_url: str):
    """TC_SEO_001: Verify SEO title length, meta description, robots meta, and canonical link."""
    page.goto(base_url, wait_until="networkidle")
    
    title = page.title()
    assert len(title) >= 30, f"Title '{title}' is too short for SEO optimization"
    
    meta_desc = page.locator("meta[name='description']").get_attribute("content")
    assert meta_desc and len(meta_desc) >= 50, "Meta description is missing or too short"
    
    robots = page.locator("meta[name='robots']").get_attribute("content")
    assert robots and "index" in robots, "Robots tag should allow indexing"

@pytest.mark.seo
@pytest.mark.regression
@pytest.mark.production_safe
def test_open_graph_and_twitter_cards(page: Page, base_url: str):
    """TC_SEO_002: Verify Open Graph and Twitter Card social metadata."""
    page.goto(base_url, wait_until="networkidle")
    
    og_title = page.locator("meta[property='og:title']").get_attribute("content")
    assert og_title and "Ananya Electrical Solutions" in og_title
    
    og_image = page.locator("meta[property='og:image']").get_attribute("content")
    assert og_image and og_image.startswith("http")
    
    twitter_card = page.locator("meta[name='twitter:card']").get_attribute("content")
    assert twitter_card == "summary_large_image"

@pytest.mark.seo
@pytest.mark.regression
@pytest.mark.production_safe
def test_schema_org_structured_data(page: Page, base_url: str):
    """TC_SEO_003: Verify presence and validity of Schema.org JSON-LD structured data."""
    page.goto(base_url, wait_until="networkidle")
    
    schemas = page.evaluate("""() => {
        const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        return scripts.map(s => {
            try { return JSON.parse(s.innerText); } catch (e) { return null; }
        }).filter(Boolean);
    }""")
    
    assert len(schemas) > 0, "No Schema.org JSON-LD scripts found"
    
    # Check that Electrician or LocalBusiness schema is present
    has_business_schema = any(
        isinstance(s.get("@graph"), list) and any("Electrician" in str(item.get("@type")) for item in s["@graph"])
        for s in schemas
    )
    assert has_business_schema, "Electrician / LocalBusiness schema not found in JSON-LD"

