from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")

    service_trigger = page.locator(".mega-menu-trigger")
    service_menu = page.locator(".mega-menu")
    service_trigger.hover()
    assert service_menu.is_visible()
    trigger_box = service_trigger.bounding_box()
    menu_box = service_menu.bounding_box()
    assert trigger_box and menu_box
    page.mouse.move(trigger_box["x"] + trigger_box["width"] / 2, trigger_box["y"] + trigger_box["height"] + 8)
    assert service_menu.is_visible(), "Service dropdown closed inside the hover gap"
    page.mouse.move(menu_box["x"] + menu_box["width"] / 2, menu_box["y"] + 30)
    service_menu.get_by_role("link", name="Bảo trì & IT Helpdesk").click()
    page.wait_for_url("**#/dich-vu/bao-tri")

    news_trigger = page.locator(".news-mega")
    news_menu = page.locator(".news-mega-menu")
    news_trigger.hover()
    assert news_menu.is_visible()
    assert news_menu.get_by_role("link", name="Thủ thuật").get_attribute("href") == "#/tin-tuc"
    assert news_menu.get_by_role("link", name="Tin tức").get_attribute("href") == "#/tin-tuc"
    trigger_box = news_trigger.bounding_box()
    menu_box = news_menu.bounding_box()
    assert trigger_box and menu_box
    page.mouse.move(trigger_box["x"] + trigger_box["width"] / 2, trigger_box["y"] + trigger_box["height"] + 8)
    assert news_menu.is_visible(), "News dropdown closed inside the hover gap"
    page.mouse.move(menu_box["x"] + menu_box["width"] / 2, menu_box["y"] + 24)
    news_menu.get_by_role("link", name="Tin tức").click()
    page.wait_for_url("**#/tin-tuc")

    assert errors == [], f"Console errors: {errors}"
    print("nav_dropdown_test: passed")
    browser.close()
