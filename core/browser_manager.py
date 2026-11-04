import os
from typing import Dict, Any, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright

class BrowserManager:
    """Manages Playwright lifecycle, browser instances, and contexts."""
    
    def __init__(self, browser_type: str = "chromium", headless: bool = True, slow_mo: int = 0):
        self.browser_type_name = browser_type.lower()
        self.headless = headless
        self.slow_mo = slow_mo
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None

    def start(self) -> BrowserContext:
        self._playwright = sync_playwright().start()
        
        launch_args = {
            "headless": self.headless,
            "slow_mo": self.slow_mo,
        }
        
        if self.browser_type_name == "firefox":
            self._browser = self._playwright.firefox.launch(**launch_args)
        elif self.browser_type_name == "webkit":
            self._browser = self._playwright.webkit.launch(**launch_args)
        else:
            self._browser = self._playwright.chromium.launch(**launch_args)

        self._context = self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True
        )
        return self._context

    def create_page(self) -> Page:
        if not self._context:
            self.start()
        return self._context.new_page()

    def close(self):
        if self._context:
            try:
                self._context.close()
            except Exception:
                pass
        if self._browser:
            try:
                self._browser.close()
            except Exception:
                pass
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass

