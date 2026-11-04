from typing import Optional, Dict
from playwright.sync_api import Page
from pages.base_page import BasePage

class ContactPage(BasePage):
    """Page Object for Consultation Quote Form and Contact Channels."""

    FORM = "#quote-form"
    INPUT_NAME = "#client-name"
    INPUT_PHONE = "#client-phone"
    SELECT_CATEGORY = "#project-type"
    INPUT_LOCATION = "#location"
    INPUT_EMAIL = "#client-email"
    BUTTON_CHANNEL_WHATSAPP = "#quote-form button:has-text('WhatsApp')"
    BUTTON_CHANNEL_EMAIL = "#quote-form button:has-text('Email')"
    TEXTAREA_NOTES = "#notes"
    CHECKBOX_COMPLIANCE = "#compliance-check"
    BUTTON_SUBMIT = "#quote-form button[type='submit']"
    
    ALERT_ERROR = "#quote-form [role='alert']"
    CONFIRMATION_BANNER = "#quote-form .bg-emerald-50"

    def __init__(self, page: Page, self_healing_engine=None):
        super().__init__(page, self_healing_engine)

    def fill_consultation_form(
        self,
        name: str,
        phone: str,
        category: str = "substation",
        location: str = "Bengaluru",
        email: Optional[str] = None,
        notes: Optional[str] = None,
        confirm_compliance: bool = True,
        preferred_channel: Optional[str] = None
    ):
        self.scroll_to_element(self.FORM)
        
        if name:
            self.fill_input(self.INPUT_NAME, name, element_key="quote_form.client_name")
        if phone:
            self.fill_input(self.INPUT_PHONE, phone, element_key="quote_form.client_phone")
        if category:
            self.page.locator(self.SELECT_CATEGORY).select_option(value=category)
        if location:
            self.fill_input(self.INPUT_LOCATION, location, element_key="quote_form.location")
        if email:
            self.fill_input(self.INPUT_EMAIL, email, element_key="quote_form.client_email")
        if notes:
            self.fill_input(self.TEXTAREA_NOTES, notes, element_key="quote_form.notes")
        if preferred_channel == "whatsapp":
            self.click_element(self.BUTTON_CHANNEL_WHATSAPP)
        elif preferred_channel == "email":
            self.click_element(self.BUTTON_CHANNEL_EMAIL)
            
        # The compliance checkbox is checked by default in React state; uncheck if False requested
        cb = self.page.locator(self.CHECKBOX_COMPLIANCE)
        if confirm_compliance is True:
            cb.check()
        elif confirm_compliance is False:
            cb.uncheck()

    def submit_form(self):
        self.click_element(self.BUTTON_SUBMIT, element_key="quote_form.submit_button")

    def get_error_message(self) -> Optional[str]:
        if self.is_visible(self.ALERT_ERROR):
            return self.get_text(self.ALERT_ERROR)
        return None

    def is_confirmation_displayed(self) -> bool:
        return self.is_visible(self.CONFIRMATION_BANNER)

    def get_confirmation_text(self) -> str:
        return self.get_text(self.CONFIRMATION_BANNER)
