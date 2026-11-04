from typing import Optional
from playwright.sync_api import Page, BrowserContext
from core.browser_manager import BrowserManager
from core.environment_manager import EnvironmentManager

class DriverFactory:
    """Factory to create isolated Playwright pages with environment awareness."""
    
    @staticmethod
    def create_driver(
        browser_type: str = "chromium",
        headless: bool = True,
        viewport: Optional[dict] = None
    ) -> tuple[BrowserManager, Page]:
        mgr = BrowserManager(browser_type=browser_type, headless=headless)
        context = mgr.start()
        if viewport:
            page = context.new_page()
            page.set_viewport_size(viewport)
        else:
            page = mgr.create_page()
        return mgr, page

