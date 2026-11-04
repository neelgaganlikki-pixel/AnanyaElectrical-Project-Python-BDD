import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.navigation_page import NavigationPage

VIEWPORTS = [
    {"name": "desktop_1920", "width": 1920, "height": 1080, "is_mobile": False},
    {"name": "desktop_1440", "width": 1440, "height": 900, "is_mobile": False},
    {"name": "tablet_768", "width": 768, "height": 1024, "is_mobile": True},
    {"name": "mobile_375", "width": 375, "height": 812, "is_mobile": True},
]

@pytest.mark.responsive
@pytest.mark.regression
@pytest.mark.parametrize("vp", VIEWPORTS)
def test_responsive_layout_reflow(page: Page, home_page: HomePage, nav_page: NavigationPage, base_url: str, vp: dict):
    """TC_RESP_001/002/003: Verify layout rendering, navbar visibility, and reflow across desktop, tablet, and mobile."""
    page.set_viewport_size({"width": vp["width"], "height": vp["height"]})
    home_page.navigate_to(base_url)
    
    # Check horizontal scroll overflow
    has_horizontal_overflow = page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
    assert not has_horizontal_overflow, f"Horizontal overflow detected at {vp['name']} ({vp['width']}x{vp['height']})"
    
    # Check mobile menu vs desktop menu
    menu_btn = page.locator("header button:has-text('menu')")
    if vp["is_mobile"]:
        expect(menu_btn).to_be_visible()
    else:
        expect(menu_btn).to_be_hidden()

