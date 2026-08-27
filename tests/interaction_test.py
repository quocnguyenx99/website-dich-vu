from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")

    root_text = page.locator(".page-home").evaluate(
        "node => [...node.childNodes].filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent.trim()).filter(Boolean)"
    )
    assert root_text == [], f"Visible export labels remain: {root_text}"

    page.get_by_role("button", name="Khám phá dịch vụ").click()
    page.wait_for_timeout(500)
    assert page.locator("#dich-vu").evaluate("node => Math.abs(node.getBoundingClientRect().top) < 160")

    page.get_by_role("button", name="XEM CHI TIẾT").first.click()
    page.wait_for_url("**#/dich-vu/chi-tiet")

    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    page.locator("#news-carousel a").first.click()
    page.wait_for_url("**#/tin-tuc/chi-tiet")

    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    page.locator(".page-home form").evaluate(
        "form => form.dispatchEvent(new SubmitEvent('submit', { bubbles: true, cancelable: true }))"
    )
    assert page.locator(".page-home .demo-form-status").is_visible()

    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    mobile.goto("http://127.0.0.1:5173/#/")
    mobile.wait_for_load_state("networkidle")
    mobile.get_by_role("button", name="Mở menu").click()
    mobile.locator('nav a[href="#/dich-vu/bao-tri"]:visible').click()
    mobile.wait_for_url("**#/dich-vu/bao-tri")
    assert mobile.locator("body").evaluate("node => node.scrollWidth") == 390

    assert errors == [], f"Console errors: {errors}"
    print("interaction_test: passed")
    browser.close()
