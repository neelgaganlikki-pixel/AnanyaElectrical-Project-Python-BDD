import pytest
from pytest_bdd import scenarios, when, then, parsers
from pages.navigation_page import NavigationPage

scenarios("../features/navigation.feature")

@when("I click the Enquiry Forms button in the header")
def click_enquiry_forms_button(nav_page: NavigationPage):
    nav_page.open_enquiry_forms_hub()

@then("the enquiry hub drawer should be visible")
def verify_drawer_visible(nav_page: NavigationPage):
    assert nav_page.is_enquiry_hub_open() is True

@then(parsers.parse("the drawer should display {count:d} modular inquiry options"))
def verify_drawer_count(nav_page: NavigationPage, count: int):
    actual_count = nav_page.get_enquiry_hub_card_count()
    assert actual_count == count, f"Expected {count} modular forms, but found {actual_count}"

