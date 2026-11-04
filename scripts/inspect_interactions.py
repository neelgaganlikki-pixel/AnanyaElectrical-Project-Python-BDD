import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(DEV_URL, wait_until="networkidle")

    print("Title:", page.title())

    # Click Enquiry Forms button
    enquiry_btn = page.locator("button:has-text('Enquiry Forms')").first
    if enquiry_btn.is_visible():
        print("Clicking Enquiry Forms button...")
        enquiry_btn.click()
        page.wait_for_timeout(1000)
        # Check if modal/dialog appeared
        modals = page.locator("[role='dialog'], .modal, [aria-modal='true'], div[class*='fixed']").all()
        print(f"Modals found after clicking Enquiry Forms: {len(modals)}")
        for i, m in enumerate(modals):
            if m.is_visible():
                print(f"Visible Modal #{i}: text='{m.inner_text()[:200]}'")

    # Let's inspect 3D Model dropdown
    model_btn = page.locator("header button:has-text('3D Model')").first
    if model_btn.is_visible():
        print("\nClicking 3D Model button...")
        model_btn.click()
        page.wait_for_timeout(500)
        dropdown_items = page.locator("header div[class*='absolute'] button, header div[class*='absolute'] a").all()
        print(f"Dropdown items found: {len(dropdown_items)}")
        for item in dropdown_items:
            if item.is_visible():
                print(f"  Item: '{item.inner_text()}'")

    # Let's inspect Services dropdown
    services_btn = page.locator("header button:has-text('Services')").first
    if services_btn.is_visible():
        print("\nClicking Services button...")
        services_btn.click()
        page.wait_for_timeout(500)
        dropdown_items = page.locator("header div[class*='absolute'] button, header div[class*='absolute'] a").all()
        for item in dropdown_items:
            if item.is_visible():
                print(f"  Services Item: '{item.inner_text()}'")

    browser.close()

