import pytest
from playwright.sync_api import Page
from pages.navigation_page import NavigationPage

@pytest.mark.functional
@pytest.mark.production_safe
def test_substation_modular_card_interaction(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_HUB_004: Verify Substation & HT modular form card exists in Enquiry Forms drawer catalog."""
    nav_page.navigate_to(base_url)
    nav_page.open_enquiry_forms_hub()
    
    # Check dialog is open
    assert nav_page.is_enquiry_hub_open()
    cards = page.locator("[role='dialog'][aria-modal='true'] span:has-text('Open Modal')")
    assert cards.count() >= 5
    
    # Substation card exists in catalog
    dialog_text = page.locator("[role='dialog'][aria-modal='true']").inner_text()
    assert "Substation" in dialog_text or "HT" in dialog_text or "11kV" in dialog_text
    
    nav_page.close_enquiry_forms_hub()

@pytest.mark.functional
@pytest.mark.production_safe
def test_solar_rooftop_modular_card_interaction(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_HUB_005: Verify Solar Rooftop EPC modular card exists in Enquiry Forms catalog."""
    nav_page.navigate_to(base_url)
    nav_page.open_enquiry_forms_hub()
    
    dialog_text = page.locator("[role='dialog'][aria-modal='true']").inner_text()
    assert "Solar" in dialog_text or "Rooftop" in dialog_text or "EPC" in dialog_text
    
    nav_page.close_enquiry_forms_hub()

@pytest.mark.functional
@pytest.mark.production_safe
def test_preventive_maintenance_card_interaction(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_HUB_006: Verify Preventive Maintenance & AMC modular card exists in Enquiry Forms catalog."""
    nav_page.navigate_to(base_url)
    nav_page.open_enquiry_forms_hub()
    
    dialog_text = page.locator("[role='dialog'][aria-modal='true']").inner_text()
    assert "Maintenance" in dialog_text or "AMC" in dialog_text or "Audit" in dialog_text
    
    nav_page.close_enquiry_forms_hub()

@pytest.mark.functional
@pytest.mark.production_safe
def test_transformer_switchgear_card_interaction(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_HUB_007: Verify Transformer & Switchgear Panel erection modular card exists in catalog."""
    nav_page.navigate_to(base_url)
    nav_page.open_enquiry_forms_hub()
    
    dialog_text = page.locator("[role='dialog'][aria-modal='true']").inner_text().lower()
    assert "transformer" in dialog_text or "switchgear" in dialog_text or "panel" in dialog_text
    
    nav_page.close_enquiry_forms_hub()

@pytest.mark.functional
@pytest.mark.production_safe
def test_statutory_liaison_card_interaction(page: Page, nav_page: NavigationPage, base_url: str):
    """TC_HUB_008: Verify CEIG/BESCOM Statutory Liaison modular card exists in catalog."""
    nav_page.navigate_to(base_url)
    nav_page.open_enquiry_forms_hub()
    
    dialog_text = page.locator("[role='dialog'][aria-modal='true']").inner_text()
    assert "CEIG" in dialog_text or "BESCOM" in dialog_text or "Liaison" in dialog_text or "Statutory" in dialog_text
    
    nav_page.close_enquiry_forms_hub()
