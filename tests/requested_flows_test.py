from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    # Dropdown closes immediately after selecting a route.
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    page.locator(".mega-menu-trigger").hover()
    page.locator(".mega-menu").get_by_role("link", name="Bảo trì & IT Helpdesk").click()
    page.wait_for_url("**#/dich-vu/bao-tri")
    assert page.locator(".mega-menu").is_hidden()

    # Home category navigation scrolls to the matching section without changing route.
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    page.locator('#dich-vu > div:first-child a[href="#home-service-deployment"]').click()
    page.wait_for_timeout(700)
    assert page.url.endswith("#/")
    target_top = page.locator("#home-service-deployment").evaluate("node => node.getBoundingClientRect().top")
    assert 0 <= target_top <= 180, target_top

    # Header consultation CTA scrolls to the current page's consultation form.
    page.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
    page.wait_for_load_state("networkidle")
    page.locator("nav").get_by_role("link", name="Nhận tư vấn").click()
    page.wait_for_timeout(700)
    tel_input = page.locator('.legacy-page input[type="tel"]').first
    assert tel_input.is_visible()
    assert tel_input.evaluate("node => node.getBoundingClientRect().top") < 900
    assert page.url.endswith("#/dich-vu/thue-thiet-bi")

    # A page without a consultation form falls back to the contact form.
    page.goto("http://127.0.0.1:5173/#/dich-vu/chi-tiet")
    page.wait_for_load_state("networkidle")
    page.locator("nav").get_by_role("link", name="Nhận tư vấn").click()
    page.wait_for_url("**#/lien-he")
    page.wait_for_timeout(700)
    assert page.locator('.page-contact input[type="tel"]').is_visible()

    # Deployment cards render three per desktop row.
    page.goto("http://127.0.0.1:5173/#/dich-vu/thi-cong")
    page.wait_for_load_state("networkidle")
    cards = page.locator(".page-deployment #services .lg\\:grid-cols-4 > div")
    assert cards.count() == 4
    card_y = [round(cards.nth(index).bounding_box()["y"]) for index in range(4)]
    assert card_y[0] == card_y[1] == card_y[2]
    assert card_y[3] > card_y[2]

    # The updated listing page is distinct from the sample article detail.
    page.goto("http://127.0.0.1:5173/#/tin-tuc")
    page.wait_for_load_state("networkidle")
    assert page.locator(".page-news article").count() == 3
    assert page.get_by_role("heading", name="TIN TỨC - KIẾN THỨC").is_visible()
    page.locator(".page-news article").first.get_by_role("link", name="Xem thêm").click()
    page.wait_for_url("**#/tin-tuc/chi-tiet")
    page.wait_for_selector(".page-news-detail")
    assert page.locator(".page-news-detail article").is_visible()
    assert page.get_by_text("NỘI DUNG BÀI VIẾT").is_visible()

    # About menu has two clearly disabled placeholders and Home remains the parent route.
    page.locator(".about-mega").hover()
    about_menu = page.locator(".about-mega > div")
    assert about_menu.is_visible()
    assert about_menu.get_by_text("Về Chính Nhân").is_visible()
    assert about_menu.get_by_text("Đội ngũ kỹ thuật").is_visible()
    assert page.locator(".about-mega > a").get_attribute("href") == "#/"

    # Contact map is no longer washed out by the former 60-80% white overlay.
    page.goto("http://127.0.0.1:5173/#/lien-he")
    page.wait_for_load_state("networkidle")
    assert page.locator(".page-contact main > section:first-child > img").get_attribute("src") == "/assets/contact-map.jpg"
    map_overlay = page.locator(".page-contact main > section:first-child > div.absolute.inset-0")
    assert float(map_overlay.evaluate("node => getComputedStyle(node).opacity")) <= 0.32
    map_filter = page.locator(".page-contact main > section:first-child > img").evaluate("node => getComputedStyle(node).filter")
    assert "contrast" in map_filter and "saturate" in map_filter

    assert errors == [], f"Console errors: {errors}"
    print("requested_flows_test: passed")
    browser.close()
