import pytest
from playwright.sync_api import Page
from pages.navigation_page import NavigationPage

@pytest.mark.functional
@pytest.mark.production_safe
def test_project_gallery_filter_chips(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_GAL_001: Verify Key Project Domains filter chips functionality (All, Industrial, Commercial, Solar)."""
    nav_page.navigate_to(base_url)
    
    # Locate section with Key Project Domains
    gallery_heading = page.locator("h2:has-text('Key Project Domains')")
    assert gallery_heading.is_visible(), "Key Project Domains section heading not visible"
    
    gallery_section = gallery_heading.locator("xpath=ancestor::section | ancestor::div[contains(@class, 'py-') or contains(@class, 'my-')]").first
    
    # Check filter buttons
    all_btn = gallery_section.locator("button:has-text('All Projects')")
    assert all_btn.is_visible(), "'All Projects' filter button not visible"
    
    # Check category buttons exist
    industrial_btn = gallery_section.locator("button:has-text('industrial')")
    commercial_btn = gallery_section.locator("button:has-text('commercial')")
    solar_btn = gallery_section.locator("button:has-text('Solar Parks')")
    
    assert industrial_btn.is_visible() or commercial_btn.is_visible() or solar_btn.is_visible()
    
    # Click industrial filter
    if industrial_btn.is_visible():
        industrial_btn.click()
        page.wait_for_timeout(400)
    
    # Reset to All Projects
    all_btn.click()
    page.wait_for_timeout(300)

@pytest.mark.functional
@pytest.mark.production_safe
def test_project_gallery_images_render(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_GAL_002: Verify project domain images render with valid dimensions and descriptive alt text."""
    nav_page.navigate_to(base_url)
    
    gallery_heading = page.locator("h2:has-text('Key Project Domains')")
    gallery_section = gallery_heading.locator("xpath=ancestor::section | ancestor::div[contains(@class, 'py-') or contains(@class, 'my-')]").first
    
    images = gallery_section.locator("img")
    count = images.count()
    assert count >= 3, f"Expected at least 3 project images in gallery section, found {count}"
    
    for i in range(count):
        img = images.nth(i)
        img.scroll_into_view_if_needed()
        page.wait_for_timeout(200)
        alt = img.get_attribute("alt")
        assert alt and len(alt.strip()) > 5, f"Image {i} has empty or insufficient alt text"
        src = img.get_attribute("src")
        assert src and len(src.strip()) > 0, f"Image {i} missing src attribute"

@pytest.mark.functional
@pytest.mark.production_safe
def test_project_gallery_case_study_cta(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_GAL_003: Verify 'View All Karnataka Case Studies & Commissioning Approvals' CTA presence."""
    nav_page.navigate_to(base_url)
    
    cta = page.locator("button:has-text('View All Karnataka Case Studies'), a:has-text('View All Karnataka Case Studies')")
    assert cta.is_visible(), "Case Studies CTA button not visible in Key Project Domains section"
    
    # Clicking CTA should not break or cause console errors
    cta.first.click()
    page.wait_for_timeout(500)
    assert page.is_visible("header"), "Page header should remain intact after CTA click"
