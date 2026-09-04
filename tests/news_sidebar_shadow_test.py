from pathlib import Path

from playwright.sync_api import sync_playwright


CASES = (
    ("/tin-tuc", ".page-news aside > div.bg-white", 3),
    ("/tin-tuc/chi-tiet", ".page-news-detail aside > div.bg-surface", 3),
)

Path("test-results").mkdir(exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)

    for width in (320, 768, 1440):
        page = browser.new_page(viewport={"width": width, "height": 900})
        console_errors = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)

        for route, selector, expected_count in CASES:
            page.goto(f"http://127.0.0.1:5173/#{route}")
            page.wait_for_load_state("networkidle")
            widgets = page.locator(selector)
            assert widgets.count() == expected_count, (width, route, widgets.count())
            assert widgets.evaluate_all(
                """nodes => nodes.every(node => {
                    const style = getComputedStyle(node)
                    return style.boxShadow !== 'none'
                        && style.borderTopWidth === '1px'
                        && node.scrollWidth <= node.clientWidth
                })"""
            ), (width, route)

        assert not console_errors, console_errors
        page.close()

    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:5173/#/tin-tuc")
    page.wait_for_load_state("networkidle")
    page.locator(".page-news aside").screenshot(path="test-results/news-sidebar-shadow.png")
    page.goto("http://127.0.0.1:5173/#/tin-tuc/chi-tiet")
    page.wait_for_load_state("networkidle")
    page.locator(".page-news-detail aside").screenshot(path="test-results/news-detail-sidebar-shadow.png")
    page.close()
    browser.close()

print("Verified 6 sidebar widgets at 320px, 768px and 1440px.")
