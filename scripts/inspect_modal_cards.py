import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(DEV_URL, wait_until="networkidle")
    page.locator("header button:has-text('Enquiry Forms')").first.click()
    page.wait_for_timeout(1000)
    
    modal = page.locator("[role='dialog'][aria-modal='true']").first
    print("Modal is visible:", modal.is_visible())
    
    # Check elements containing 'Open Modal'
    open_modal_spans = modal.locator("span:has-text('Open Modal')")
    print("span:has-text('Open Modal') count:", open_modal_spans.count())
    
    # Check cards
    cards = modal.locator("div.p-4, div.rounded-xl, div.border").all()
    print("Candidate card divs:", len(cards))
    
    # Let's inspect unique texts of the cards
    forms = modal.locator("h4, h3").all()
    print(f"Form titles (h3/h4) count: {len(forms)}")
    for f in forms:
        print("  Form title:", f.inner_text().strip())
        
    browser.close()

