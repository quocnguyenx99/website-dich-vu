import json

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
    "mobile": {"width": 390, "height": 844},
    "tablet": {"width": 768, "height": 1024},
    "desktop": {"width": 1440, "height": 900},
}

MEASURE = """() => {
  const visible = element => {
    const style = getComputedStyle(element)
    const rect = element.getBoundingClientRect()
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0
  }
  const values = (selector, property) => [...document.querySelectorAll(selector)]
    .filter(visible)
    .map(element => Math.round(parseFloat(getComputedStyle(element)[property]) || 0))
  const imageHeights = [...document.querySelectorAll('.legacy-page img')]
    .filter(visible)
    .filter(image => getComputedStyle(image).position !== 'absolute')
    .map(image => Math.round(image.getBoundingClientRect().height))
  const sectionPadding = [...document.querySelectorAll('.legacy-page section')]
    .filter(visible)
    .map(section => {
      const style = getComputedStyle(section)
      return Math.round(parseFloat(style.paddingTop) + parseFloat(style.paddingBottom))
    })
  const h1 = values('.legacy-page h1', 'fontSize')
  const h2 = values('.legacy-page h2', 'fontSize')
  return {
    height: document.documentElement.scrollHeight,
    maxH1: Math.max(0, ...h1),
    maxH2: Math.max(0, ...h2),
    maxImage: Math.max(0, ...imageHeights),
    largeImages: imageHeights.filter(height => height >= 400).length,
    averageSectionPadding: sectionPadding.length
      ? Math.round(sectionPadding.reduce((sum, value) => sum + value, 0) / sectionPadding.length)
      : 0,
  }
}"""


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    results = {}

    for viewport_name, viewport in VIEWPORTS.items():
        page = browser.new_page(viewport=viewport)
        results[viewport_name] = {}
        for name, route in ROUTES.items():
            page.goto(f"http://127.0.0.1:5173/#{route}")
            page.wait_for_load_state("networkidle")
            results[viewport_name][name] = page.evaluate(MEASURE)
        page.close()

    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
    page.wait_for_load_state("networkidle")
    page.locator("nav").first.evaluate("element => element.style.display = 'none'")
    page.locator("#services .card-hover").first.screenshot(path="test-results/compact-service-card-desktop.png")
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    page.locator("nav").first.evaluate("element => element.style.display = 'none'")
    page.locator("#home-service-rental").screenshot(path="test-results/compact-home-service-desktop.png")
    page.close()

    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
    page.wait_for_load_state("networkidle")
    page.locator("nav").first.evaluate("element => element.style.display = 'none'")
    page.locator("#services .card-hover").first.screenshot(path="test-results/compact-service-card-mobile.png")
    page.close()

    browser.close()

print(json.dumps(results, ensure_ascii=True))
