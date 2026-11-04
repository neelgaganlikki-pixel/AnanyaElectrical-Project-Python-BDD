from typing import Optional, Any
from playwright.sync_api import Page, Locator
from core.self_healing_engine import SelfHealingEngine
from utils.logger import get_logger
from utils.screenshots import take_screenshot

class BasePage:
    """Base Page Object providing unified interactions, logging, screenshots, and self-healing integration."""

    def __init__(self, page: Page, self_healing_engine: Optional[SelfHealingEngine] = None):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)
        self.healer = self_healing_engine or SelfHealingEngine(mode="ASSISTED")

    def navigate_to(self, url: str):
        self.logger.info(f"Navigating to: {url}")
        response = self.page.goto(url, wait_until="networkidle")
        return response

    def click_element(self, selector: str, element_key: Optional[str] = None):
        self.logger.info(f"Clicking element: '{selector}' (key: {element_key})")
        if element_key:
            return self.healer.resolve_and_execute(self.page, element_key=element_key, action="click")
        return self.page.locator(selector).click()

    def fill_input(self, selector: str, value: str, element_key: Optional[str] = None):
        self.logger.info(f"Filling input '{selector}' with: '{value}' (key: {element_key})")
        if element_key:
            return self.healer.resolve_and_execute(self.page, element_key=element_key, action="fill", action_arg=value)
        return self.page.locator(selector).fill(value)

    def get_text(self, selector: str, element_key: Optional[str] = None) -> str:
        if element_key:
            return self.healer.resolve_and_execute(self.page, element_key=element_key, action="get_text")
        return self.page.locator(selector).inner_text().strip()

    def is_visible(self, selector: str, element_key: Optional[str] = None) -> bool:
        if element_key:
            try:
                return self.healer.resolve_and_execute(self.page, element_key=element_key, action="is_visible")
            except Exception:
                return False
        return self.page.locator(selector).is_visible()

    def wait_for_element(self, selector: str, state: str = "visible", timeout_ms: int = 10000):
        return self.page.locator(selector).wait_for(state=state, timeout=timeout_ms)

    def get_element_attribute(self, selector: str, attribute_name: str) -> Optional[str]:
        return self.page.locator(selector).get_attribute(attribute_name)

    def scroll_to_element(self, selector: str):
        self.page.locator(selector).scroll_into_view_if_needed()

    def take_screenshot(self, name_prefix: str) -> str:
        return take_screenshot(self.page, name_prefix)

