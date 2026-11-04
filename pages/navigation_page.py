import re
from playwright.sync_api import Page
from pages.base_page import BasePage

class NavigationPage(BasePage):
    """Page Object for Header Navigation, Dropdowns, Hamburger Menu, and Modal Catalogs."""

    NAV_3D_MODEL = "header button:has-text('3D Model')"
    NAV_SERVICES = "header button:has-text('Services')"
    NAV_PROJECTS = "header button:has-text('Projects Gallery')"
    NAV_ABOUT_US = "header button:has-text('About Us')"
    NAV_CONTACT_US = "header button:has-text('Contact Us')"
    NAV_ENQUIRY_FORMS = "header button:has-text('Enquiry Forms')"
    NAV_GET_QUOTE = "header button:has-text('Get a Consultation / Quote'), header button:has-text('Get Quote')"
    NAV_MOBILE_MENU_BUTTON = "header button:has-text('menu')"
    
    MODAL_ENQUIRY_HUB = "[role='dialog'][aria-modal='true']"
    MODAL_CLOSE_BUTTON = "[role='dialog'][aria-modal='true'] button:has-text('close')"
    MODAL_CARDS = "[role='dialog'][aria-modal='true'] span:has-text('Open Modal')"

    def __init__(self, page: Page, self_healing_engine=None):
        super().__init__(page, self_healing_engine)

    def click_about_us(self):
        self.click_element(self.NAV_ABOUT_US, element_key="navigation.about_us_link")

    def click_contact_us(self):
        self.click_element(self.NAV_CONTACT_US, element_key="navigation.contact_us_link")

    def open_enquiry_forms_hub(self):
        self.click_element(self.NAV_ENQUIRY_FORMS, element_key="navigation.enquiry_forms_button")
        self.wait_for_element(self.MODAL_ENQUIRY_HUB)

    def close_enquiry_forms_hub(self):
        self.click_element(self.MODAL_CLOSE_BUTTON)

    def is_enquiry_hub_open(self) -> bool:
        return self.is_visible(self.MODAL_ENQUIRY_HUB)

    def get_enquiry_hub_card_count(self) -> int:
        return self.page.locator(self.MODAL_CARDS).count()

    def is_mobile_menu_button_visible(self) -> bool:
        return self.is_visible(self.NAV_MOBILE_MENU_BUTTON)
