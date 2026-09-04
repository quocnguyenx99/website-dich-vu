from playwright.sync_api import sync_playwright


ROUTES = [
    "/",
    "/dich-vu/thue-thiet-bi",
    "/dich-vu/bao-tri",
    "/dich-vu/sua-chua",
    "/dich-vu/thi-cong",
    "/dich-vu/chi-tiet",
    "/tin-tuc",
    "/tin-tuc/chi-tiet",
    "/tuyen-dung",
    "/lien-he",
]

BAD_ENCODING_MARKERS = ("\ufffd", "\u00c3", "\u00c6")


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    failures = []

    for route in ROUTES:
        page.goto(f"http://localhost:5173/#{route}")
        page.wait_for_load_state("networkidle")
        text = page.locator("body").inner_text()
        found = [marker for marker in BAD_ENCODING_MARKERS if marker in text]
        if found:
            failures.append(f"{route}: invalid encoding marker(s) {found}")

    browser.close()

if failures:
    raise AssertionError("\n".join(failures))

print(f"Verified UTF-8 rendering on {len(ROUTES)} routes.")
