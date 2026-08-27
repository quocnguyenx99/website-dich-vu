from pathlib import Path
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


def audit(page, viewport_name: str):
    results = []
    for route in ROUTES:
        page.goto(f"http://127.0.0.1:5173/#{route}")
        page.wait_for_load_state("networkidle")
        metrics = page.evaluate(
            """() => ({
                title: document.title,
                bodyWidth: document.body.scrollWidth,
                viewportWidth: document.documentElement.clientWidth,
                buttons: document.querySelectorAll('button').length,
                buttonLabels: [...document.querySelectorAll('button')].map(button => button.innerText.replace(/\\s+/g, ' ').trim()),
                links: document.querySelectorAll('a').length,
                emptyLinks: [...document.querySelectorAll('a')].filter(a => (a.getAttribute('href') || '') === '#').length,
                emptyLinkLabels: [...document.querySelectorAll('a')].filter(a => (a.getAttribute('href') || '') === '#').map(a => a.innerText.replace(/\\s+/g, ' ').trim()),
                forms: document.querySelectorAll('form').length,
                brokenImages: [...document.images].filter(img => img.complete && img.naturalWidth === 0).length,
            })"""
        )
        metrics["route"] = route
        metrics["overflow"] = metrics["bodyWidth"] - metrics["viewportWidth"]
        results.append(metrics)

    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    Path("test-results").mkdir(exist_ok=True)
    page.screenshot(path=f"test-results/home-{viewport_name}.png", full_page=True)
    return results


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    console_errors = []

    for viewport_name, size in (
        ("desktop", {"width": 1440, "height": 900}),
        ("mobile", {"width": 390, "height": 844}),
    ):
        page = browser.new_page(viewport=size)
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        print(viewport_name, audit(page, viewport_name))
        page.close()

    print("console_errors", console_errors)
    browser.close()
