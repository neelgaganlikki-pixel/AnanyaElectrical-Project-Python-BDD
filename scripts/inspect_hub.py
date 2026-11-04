import sys
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(DEV_URL, wait_until="networkidle")

    # Click Enquiry Forms button
    enquiry_btn = page.locator("button:has-text('Enquiry Forms')").first
    enquiry_btn.click()
    page.wait_for_timeout(1000)

    # Extract all elements inside the modal
    modal = page.locator("[role='dialog'][aria-modal='true']").first
    print("Modal is visible:", modal.is_visible())

    # Get all form cards / buttons inside the modal
    cards = modal.locator("button, a").all()
    print(f"Interactive elements inside modal: {len(cards)}")
    for i, c in enumerate(cards):
        text = c.inner_text().strip().replace('\n', ' ')
        if text:
            print(f"  Item #{i}: {text}")

    # Close modal
    close_btn = modal.locator("button:has-text('close')").first
    if close_btn.is_visible():
        print("Closing modal...")
        close_btn.click()
        page.wait_for_timeout(500)

    # Now inspect dropdowns without modal blocking
    # 1. 3D Model
    print("\n--- Testing 3D Model dropdown ---")
    model_btn = page.locator("header button:has-text('3D Model')").first
    model_btn.click()
    page.wait_for_timeout(500)
    dropdown_buttons = page.locator("header").locator("button, a").all()
    for b in dropdown_buttons:
        txt = b.inner_text().strip().replace('\n', ' ')
        if "3D" in txt or "Substation" in txt or "Interior" in txt or "Solar" in txt:
            print("  3D dropdown item:", txt)

    # 2. Services dropdown
    print("\n--- Testing Services dropdown ---")
    services_btn = page.locator("header button:has-text('Services')").first
    services_btn.click()
    page.wait_for_timeout(500)
    for b in page.locator("header").locator("button, a").all():
        txt = b.inner_text().strip().replace('\n', ' ')
        if any(w in txt for w in ["HT", "LT", "Transformer", "Solar", "Panel"]):
            print("  Services dropdown item:", txt)

    browser.close()

