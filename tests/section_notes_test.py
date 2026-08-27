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


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    findings = {}

    for route in ROUTES:
        page.goto(f"http://127.0.0.1:5173/#{route}")
        page.wait_for_load_state("networkidle")
        notes = page.locator(".legacy-page").evaluate(
            "root => [...root.childNodes].filter(node => node.nodeType === Node.TEXT_NODE).map(node => node.textContent.replace(/\\s+/g, ' ').trim()).filter(Boolean)"
        )
        if notes:
            findings[route] = notes

    assert findings == {}, f"Visible export notes remain: {findings}"
    print("section_notes_test: passed")
    browser.close()
