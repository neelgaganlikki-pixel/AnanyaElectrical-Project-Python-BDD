import re
from typing import Optional
from playwright.sync_api import Page
from pages.base_page import BasePage

class HomePage(BasePage):
    """Page Object for Ananya Electrical Solutions Homepage."""

    # Selectors
    HEADER = "header"
    BRAND_LOGO = "header button:has-text('ANANYA')"
    HERO_HEADING = "h1"
    HERO_PHONE_CTA = "section a[href='tel:+919632025123']"
    HERO_WHATSAPP_CTA = "section a[href*='wa.me']"
    SECTION_SERVICES = "#services"
    SECTION_ELECTRICAL = "#electrical-services"
    SECTION_ABOUT = "#about-us"
    SECTION_CONSULTATION = "#consultation"
    SECTION_AREAS = "#service-areas"
    FOOTER = "footer"

    def __init__(self, page: Page, self_healing_engine=None):
        super().__init__(page, self_healing_engine)

    def get_hero_title(self) -> str:
        return self.get_text(self.HERO_HEADING)

    def click_brand_logo(self):
        self.click_element(self.BRAND_LOGO)

    def is_footer_visible(self) -> bool:
        self.scroll_to_element(self.FOOTER)
        return self.is_visible(self.FOOTER)

    def get_footer_text(self) -> str:
        return self.get_text(self.FOOTER)

    def is_header_sticky(self) -> bool:
        # Check class and bounding box after scroll
        self.page.evaluate("window.scrollTo(0, 1500)")
        self.page.wait_for_timeout(300)
        box = self.page.locator(self.HEADER).bounding_box()
        return box is not None and box["y"] <= 0

