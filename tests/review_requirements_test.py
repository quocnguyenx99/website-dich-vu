from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")

    flags = page.locator(".language-flags img:visible")
    assert flags.count() == 2
    assert flags.nth(0).get_attribute("src") == "/assets/flags/vi.svg"
    assert flags.nth(1).get_attribute("src") == "/assets/flags/en.svg"

    font_families = page.locator("body").evaluate(
        """body => [...body.querySelectorAll('h1, h2, h3, p, a, button, input')]
          .filter(el => !el.classList.contains('material-symbols-outlined'))
          .map(el => getComputedStyle(el).fontFamily)"""
    )
    assert font_families
    assert all(font.startswith("Inter") for font in font_families), set(font_families)
    assert page.evaluate("document.fonts.check('16px Inter')")

    page.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
    page.wait_for_load_state("networkidle")
    page.get_by_role("link", name="XEM THÊM").first.click()
    page.wait_for_url("**#/dich-vu/chi-tiet")

    print("review_requirements_test: passed")
    browser.close()
