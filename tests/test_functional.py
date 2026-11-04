import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.navigation_page import NavigationPage

@pytest.mark.smoke
@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.production_safe
def test_homepage_loads_successfully(page: Page, home_page: HomePage, base_url: str):
    """TC_FUNC_001: Verify homepage loads successfully with status 200 and expected title."""
    response = home_page.navigate_to(base_url)
    assert response.status == 200, f"Expected status 200 but received {response.status}"
    
    title = page.title()
    assert "Electrical Contractor in Bengaluru" in title, f"Title mismatch: '{title}'"
    assert "Ananya Electrical Solutions" in title

@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.production_safe
def test_brand_logo_navigation(page: Page, home_page: HomePage, base_url: str):
    """TC_FUNC_002: Verify brand logo presence and click action resets viewport to top."""
    home_page.navigate_to(base_url)
    # Scroll down 1000px
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(300)
    
    # Click logo
    home_page.click_brand_logo()
    page.wait_for_timeout(1200)
    
    # Verify smooth scroll returned to top
    scroll_y = page.evaluate("window.scrollY")
    assert scroll_y < 150, f"Expected scroll position near 0, but was {scroll_y}"

@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.production_safe
def test_desktop_navigation_scroll(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_FUNC_003: Verify desktop navigation links mount corresponding page views."""
    nav_page.navigate_to(base_url)
    
    # Navigate to About Us
    nav_page.click_about_us()
    page.wait_for_timeout(800)
    # About Us view displays Class 1 contractor / credentials
    about_text = page.locator("body").inner_text()
    assert "Super Grade" in about_text or "Class 1" in about_text or "Sahakarnagar" in about_text

    # Navigate to Contact Us
    nav_page.click_contact_us()
    page.wait_for_timeout(800)
    contact_text = page.locator("body").inner_text()
    assert "9632025123" in contact_text or "Quote" in contact_text

@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.production_safe
def test_enquiry_forms_hub_drawer(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_FUNC_004: Verify clicking 'Enquiry Forms' button opens modal catalog with 15 forms."""
    nav_page.navigate_to(base_url)
    
    nav_page.open_enquiry_forms_hub()
    assert nav_page.is_enquiry_hub_open(), "Modal catalog did not open"
    
    card_count = nav_page.get_enquiry_hub_card_count()
    assert card_count == 15, f"Expected 15 form cards in catalog, found {card_count}"
    
    nav_page.close_enquiry_forms_hub()
    page.wait_for_timeout(500)
    assert not nav_page.is_enquiry_hub_open(), "Modal catalog did not close"

@pytest.mark.functional
@pytest.mark.regression
@pytest.mark.production_safe
def test_sticky_header_behavior(page: Page, home_page: HomePage, base_url: str):
    """TC_FUNC_005: Verify header maintains sticky fixed positioning when scrolling."""
    home_page.navigate_to(base_url)
    assert home_page.is_header_sticky(), "Header failed to remain sticky after scroll"
