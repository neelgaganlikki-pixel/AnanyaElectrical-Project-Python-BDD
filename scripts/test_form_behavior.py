import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
DEV_URL = "https://ananya-electrical-solutions.neelgaganat97.workers.dev"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})

    # Capture dialogs (alerts, confirms, prompts)
    dialogs = []
    page.on("dialog", lambda d: (dialogs.append(d.message), d.accept()))

    console_logs = []
    page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

    page.goto(DEV_URL, wait_until="networkidle")

    # Scroll to consultation form
    form = page.locator("#quote-form")
    print("Form found:", form.count() > 0)

    # Test 1: Try clicking submit button without filling fields
    submit_btn = form.locator("button[type='submit']")
    submit_btn.click()
    page.wait_for_timeout(500)
    print("Dialogs after empty submit:", dialogs)

    # Check validity of fields via JS
    validity = page.evaluate('''() => {
        const name = document.getElementById('client-name');
        const phone = document.getElementById('client-phone');
        return {
            name_valid: name.checkValidity(),
            name_validationMessage: name.validationMessage,
            phone_valid: phone.checkValidity()
        };
    }''')
    print("HTML5 Validity check:", validity)

    # Check WhatsApp button inside form
    wa_btn = form.locator("button:has-text('WhatsApp')")
    print("WhatsApp button in form count:", wa_btn.count())

    # Check Email button inside form
    email_btn = form.locator("button:has-text('Email')")
    print("Email button in form count:", email_btn.count())

    browser.close()

