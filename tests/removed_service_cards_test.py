from playwright.sync_api import sync_playwright


CHECKS = {
    "/dich-vu/bao-tri": "Bảo trì hệ thống mail",
    "/dich-vu/sua-chua": "Sửa chữa lắp đặt camera",
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    for route, removed_card_title in CHECKS.items():
        page.goto(f"http://localhost:5173/#{route}")
        page.wait_for_load_state("networkidle")
        assert removed_card_title not in page.locator("body").inner_text(), f"{removed_card_title} is still displayed on {route}"

    browser.close()

print("Verified that both requested service cards are absent.")
