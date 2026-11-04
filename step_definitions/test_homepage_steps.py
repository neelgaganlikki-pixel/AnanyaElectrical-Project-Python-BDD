import pytest
from pytest_bdd import scenarios, then, parsers
from playwright.sync_api import Page, expect

scenarios("../features/homepage.feature")

@then(parsers.parse('the page title should contain "{expected_text}"'))
def verify_title(page: Page, expected_text: str):
    assert expected_text in page.title()

@then("the brand logo should be visible in the header")
def verify_logo_visible(page: Page):
    logo = page.locator("header button:has-text('ANANYA')")
    expect(logo).to_be_visible()
