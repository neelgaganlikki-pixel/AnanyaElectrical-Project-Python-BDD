import os
import datetime
from playwright.sync_api import Page

def take_screenshot(page: Page, name_prefix: str = "screenshot") -> str:
    """Takes a full page screenshot and returns the absolute file path."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
    safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name_prefix)
    screenshot_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    file_path = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")
    page.screenshot(path=file_path, full_page=True)
    return file_path

