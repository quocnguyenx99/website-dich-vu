import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROUTES = {
    "home": "/",
    "rental": "/dich-vu/thue-thiet-bi",
    "maintenance": "/dich-vu/bao-tri",
    "repair": "/dich-vu/sua-chua",
    "deployment": "/dich-vu/thi-cong",
    "service-detail": "/dich-vu/chi-tiet",
    "news": "/tin-tuc",
    "news-detail": "/tin-tuc/chi-tiet",
    "careers": "/tuyen-dung",
    "contact": "/lien-he",
}

VIEWPORTS = {
    "mobile-small": {"width": 320, "height": 640},
    "mobile": {"width": 390, "height": 844},
    "tablet-portrait": {"width": 768, "height": 1024},
    "tablet-landscape": {"width": 1024, "height": 768},
    "desktop": {"width": 1440, "height": 900},
}

AUDIT_SCRIPT = """() => {
  const visible = element => {
    const style = getComputedStyle(element)
    const rect = element.getBoundingClientRect()
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0
  }
  const describe = element => {
    const rect = element.getBoundingClientRect()
    return {
      tag: element.tagName.toLowerCase(),
      className: typeof element.className === 'string' ? element.className.slice(0, 120) : '',
      text: (element.innerText || element.alt || '').replace(/\\s+/g, ' ').trim().slice(0, 80),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
    }
  }
  const controls = [...document.querySelectorAll('button, input, select, textarea, a.btn-primary, a.bg-primary-container')].filter(visible)
  const undersizedControls = controls.filter(element => {
    const rect = element.getBoundingClientRect()
    return rect.width < 40 || rect.height < 40
  }).map(describe)
  const clippedControls = controls.filter(element => element.scrollWidth > element.clientWidth + 1 || element.scrollHeight > element.clientHeight + 1).map(describe)
  const brokenImages = [...document.images].filter(image => image.complete && image.naturalWidth === 0).map(describe)
  const h1 = document.querySelector('.legacy-page h1')
  const firstSection = document.querySelector('.legacy-page main > section:first-child')
  return {
    viewportWidth: document.documentElement.clientWidth,
    bodyWidth: document.body.scrollWidth,
    overflow: Math.max(0, document.body.scrollWidth - document.documentElement.clientWidth),
    undersizedControls,
    clippedControls,
    brokenImages,
    h1: h1 ? describe(h1) : null,
    firstSectionHeight: firstSection ? Math.round(firstSection.getBoundingClientRect().height) : 0,
  }
}"""


Path("test-results/responsive").mkdir(parents=True, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    results = {}
    console_errors = []

    for viewport_name, viewport in VIEWPORTS.items():
        page = browser.new_page(viewport=viewport)
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        results[viewport_name] = {}

        for slug, route in ROUTES.items():
            page.goto(f"http://127.0.0.1:5173/#{route}")
            page.wait_for_load_state("networkidle")
            page.evaluate("window.scrollTo(0, 0)")
            results[viewport_name][slug] = page.evaluate(AUDIT_SCRIPT)

            if viewport_name in ("mobile-small", "tablet-portrait"):
                page.screenshot(path=f"test-results/responsive/{slug}-{viewport_name}.png", full_page=False)

        page.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
        page.wait_for_load_state("networkidle")
        cards = page.locator("#services .card-hover")
        card_columns = len(set(round(cards.nth(index).bounding_box()["x"]) for index in range(min(cards.count(), 6))))
        expected_columns = 1 if viewport["width"] < 768 else 2 if viewport["width"] < 1024 else 3
        assert card_columns == expected_columns, (viewport_name, card_columns, expected_columns)

        mobile_menu_button = page.locator('nav button[aria-controls="mobile-navigation"]')
        if viewport["width"] < 1280:
            assert mobile_menu_button.is_visible(), viewport_name
            mobile_menu_button.click()
            mobile_navigation = page.locator("#mobile-navigation")
            assert mobile_navigation.is_visible(), viewport_name
            assert mobile_navigation.evaluate("node => node.scrollWidth <= node.clientWidth"), viewport_name
        else:
            assert not mobile_menu_button.is_visible(), viewport_name
            assert page.locator("nav ul").first.is_visible(), viewport_name

        page.close()

    browser.close()

summary = {
    "overflow": {
        viewport: {route: data["overflow"] for route, data in routes.items() if data["overflow"]}
        for viewport, routes in results.items()
    },
    "undersizedControls": {
        viewport: {route: data["undersizedControls"] for route, data in routes.items() if data["undersizedControls"]}
        for viewport, routes in results.items()
    },
    "clippedControls": {
        viewport: {route: data["clippedControls"] for route, data in routes.items() if data["clippedControls"]}
        for viewport, routes in results.items()
    },
    "brokenImages": sum(len(data["brokenImages"]) for routes in results.values() for data in routes.values()),
    "consoleErrors": console_errors,
    "heroHeights": {
        viewport: {route: data["firstSectionHeight"] for route, data in routes.items()}
        for viewport, routes in results.items()
    },
}

print(json.dumps(summary, ensure_ascii=True))

assert all(not routes for routes in summary["overflow"].values()), summary["overflow"]
assert all(not routes for routes in summary["undersizedControls"].values()), summary["undersizedControls"]
assert all(not routes for routes in summary["clippedControls"].values()), summary["clippedControls"]
assert summary["brokenImages"] == 0, summary["brokenImages"]
assert not summary["consoleErrors"], summary["consoleErrors"]
print("Responsive checks passed for 10 routes across 5 viewport sizes.")
