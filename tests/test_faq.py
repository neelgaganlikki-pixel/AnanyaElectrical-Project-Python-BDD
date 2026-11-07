import json
import pytest
from playwright.sync_api import Page
from pages.navigation_page import NavigationPage

@pytest.mark.functional
@pytest.mark.production_safe
def test_faq_schema_entities(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_FAQ_001: Verify FAQ Schema contains 5 core statutory and engineering Q&As."""
    nav_page.navigate_to(base_url)
    
    faq_data = page.evaluate("""() => {
        const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        for (const s of scripts) {
            try {
                const parsed = JSON.parse(s.innerText);
                if (parsed['@graph']) {
                    const faq = parsed['@graph'].find(item => item['@type'] === 'FAQPage');
                    if (faq) return faq.mainEntity;
                }
            } catch (e) {}
        }
        return null;
    }""")
    
    assert faq_data is not None, "FAQPage schema not found in structured data"
    assert len(faq_data) >= 5, f"Expected at least 5 FAQ questions in schema, found {len(faq_data)}"
    
    question_names = [q.get("name") for q in faq_data]
    assert any("Super Grade Licensed Electrical Contractor" in q for q in question_names)
    assert any("CEIG drawing sanction and BESCOM" in q for q in question_names)
    assert any("Where is Ananya Electrical Solutions located" in q for q in question_names)

@pytest.mark.functional
@pytest.mark.production_safe
def test_faq_ceig_bescom_answers(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_FAQ_002: Verify statutory answers for CEIG approvals and BESCOM power energization."""
    nav_page.navigate_to(base_url)
    
    faq_data = page.evaluate("""() => {
        const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        for (const s of scripts) {
            try {
                const parsed = JSON.parse(s.innerText);
                if (parsed['@graph']) {
                    const faq = parsed['@graph'].find(item => item['@type'] === 'FAQPage');
                    if (faq) return faq.mainEntity;
                }
            } catch (e) {}
        }
        return [];
    }""")
    
    ceig_q = next((q for q in faq_data if "CEIG" in q.get("name", "")), None)
    assert ceig_q is not None, "CEIG approval FAQ not found"
    answer_text = ceig_q.get("acceptedAnswer", {}).get("text", "")
    assert "10 to 14 working days" in answer_text or "Single Line Diagrams" in answer_text

@pytest.mark.accessibility
@pytest.mark.production_safe
def test_faq_accessibility_entities(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_FAQ_003: Verify Schema entity references and SEO snippet accessibility for search crawlers."""
    nav_page.navigate_to(base_url)
    
    graph_ids = page.evaluate("""() => {
        const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
        const ids = [];
        for (const s of scripts) {
            try {
                const parsed = JSON.parse(s.innerText);
                if (parsed['@graph']) {
                    parsed['@graph'].forEach(item => {
                        if (item['@id']) ids.push(item['@id']);
                    });
                }
            } catch (e) {}
        }
        return ids;
    }""")
    
    assert any("#faq" in gid for gid in graph_ids), "FAQ anchor ID not linked in Schema graph"
    assert any("#business" in gid for gid in graph_ids), "Business ID not linked in Schema graph"

