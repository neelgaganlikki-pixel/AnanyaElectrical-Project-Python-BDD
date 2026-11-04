import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from playwright.sync_api import Page, expect

scenarios("../features/contact.feature")

@when(parsers.parse('I enter client name "{client_name}"'))
def enter_client_name(page: Page, client_name: str):
    page.locator("#client-name").fill(client_name)

@when(parsers.parse('I enter invalid phone number "{phone}"'))
def enter_invalid_phone(page: Page, phone: str):
    page.locator("#client-phone").fill(phone)

@when(parsers.parse('I enter location "{loc}"'))
def enter_location(page: Page, loc: str):
    page.locator("#location").fill(loc)

@when("I confirm KEI statutory compliance")
def confirm_compliance(page: Page):
    page.locator("#compliance-check").check()

@when("I click submit engineering inquiry")
def click_submit(page: Page):
    page.locator("#quote-form button[type='submit']").click()
    page.wait_for_timeout(500)

@then(parsers.parse('a validation alert should be displayed containing "{expected_msg}"'))
def verify_alert_displayed(page: Page, expected_msg: str):
    alert = page.locator("#quote-form [role='alert']")
    expect(alert).to_be_visible()
    assert expected_msg in alert.inner_text()

