from pathlib import Path

from playwright.sync_api import sync_playwright


output = Path("references/current-service-card.png").resolve()

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=1)
    page.goto("http://localhost:5173/#/dich-vu/thue-thiet-bi")
    page.wait_for_load_state("networkidle")
    card = page.locator(".card-hover").first
    card.scroll_into_view_if_needed()
    card.screenshot(path=str(output))
    browser.close()

print(output)
