import re

from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

    # Dropdown closes immediately after selecting a route.
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    commitment_heading = page.get_by_text("≤ 30 Phút", exact=True)
    hero_heading = page.get_by_role("heading", name=re.compile("TƯ VẤN.*THIẾT KẾ"))
    assert commitment_heading.bounding_box()["y"] < hero_heading.bounding_box()["y"]
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

    # Each Home service CTA opens its corresponding service category.
    home_service_routes = {
        "home-service-rental": "/dich-vu/thue-thiet-bi",
        "home-service-maintenance": "/dich-vu/bao-tri",
        "home-service-deployment": "/dich-vu/thi-cong",
        "home-service-repair": "/dich-vu/sua-chua",
        "home-service-outsourcing": "/dich-vu/bao-tri",
    }
    for section_id, route in home_service_routes.items():
        page.goto("http://127.0.0.1:5173/#/")
        page.wait_for_load_state("networkidle")
        page.locator(f"#{section_id}").get_by_role("button", name="XEM CHI TIẾT").click()
        page.wait_for_url(f"**#{route}")

    # Consultation form uses a main category before enabling its matching sub-service list.
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    consultation_form = page.locator(".page-home form").first
    main_service = consultation_form.locator('select[name="serviceCategory"]')
    sub_service = consultation_form.locator('select[name="subService"]')
    assert main_service.is_visible() and sub_service.is_visible()
    assert sub_service.is_disabled()
    main_service.select_option(label="Thi công & lắp đặt")
    assert not sub_service.is_disabled()
    assert sub_service.locator("option").all_text_contents() == [
        "Chọn dịch vụ cụ thể *", "Cấu hình Server", "Camera giám sát văn phòng",
        "Dịch vụ tháo lắp camera", "Dịch vụ lắp đặt camera", "Thi công camera giám sát",
    ]

    # The dependent selector remains visible directly below its parent on mobile.
    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    mobile.goto("http://127.0.0.1:5173/#/")
    mobile.wait_for_load_state("networkidle")
    mobile_form = mobile.locator(".page-home form").first
    mobile_main_service = mobile_form.locator('select[name="serviceCategory"]')
    mobile_sub_service = mobile_form.locator('select[name="subService"]')
    mobile_main_service.select_option(label="Cho thuê thiết bị")
    assert mobile_form.locator("select").count() == 3, mobile_form.locator("select").count()
    assert mobile_sub_service.is_visible() and not mobile_sub_service.is_disabled()
    assert mobile_sub_service.bounding_box()["y"] > mobile_main_service.bounding_box()["y"]
    mobile.close()

    # Header consultation CTA scrolls to the current page's consultation form.
    page.locator("nav").get_by_role("link", name="Nhận tư vấn").click()
    page.wait_for_timeout(700)
    assert consultation_form.evaluate("node => node.getBoundingClientRect().top") < 900

    # Floating quick-contact controls include social channels, hotline and delayed scroll-to-top.
    floating_contact = page.locator(".floating-contact")
    assert floating_contact.get_by_role("link").count() == 3
    scroll_top = floating_contact.get_by_role("button", name="Lên đầu trang")
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(150)
    assert not scroll_top.is_visible()
    page.evaluate("window.scrollTo(0, window.innerHeight / 3 + 40)")
    page.wait_for_timeout(150)
    assert scroll_top.is_visible()
    scroll_top.click()
    page.wait_for_timeout(300)
    scroll_y = page.evaluate("window.scrollY")
    assert scroll_y < page.evaluate("window.innerHeight / 3 + 40"), scroll_y

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

    # Deployment hero CTAs use clear sentence-case labels.
    deployment_hero = page.locator(".page-deployment main > section").first
    assert deployment_hero.get_by_role("link", name=re.compile(r"^Khám phá dịch vụ")).is_visible()
    assert deployment_hero.get_by_text("Tìm hiểu thêm", exact=True).is_visible()

    # Careers show one concise, current opening and no legacy job cards or pagination.
    page.goto("http://127.0.0.1:5173/#/tuyen-dung")
    page.wait_for_load_state("networkidle")
    careers_card = page.locator(".career-job-card")
    assert careers_card.count() == 1
    assert careers_card.get_by_role("heading", name="Nhân viên Kỹ thuật Hỗ trợ Phần cứng/Mạng").is_visible()
    assert careers_card.get_by_text(re.compile(r"Hạn nộp:\s*30/09/2026")).is_visible()
    assert page.locator(".page-careers .career-job-card + div").count() == 0

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

    # Footer links point to their matching routes, including the FAQ fallback article.
    page.goto("http://127.0.0.1:5173/#/")
    page.wait_for_load_state("networkidle")
    footer = page.locator(".site-footer")
    assert footer.get_by_role("link", name="Bảo trì & Helpdesk").get_attribute("href") == "#/dich-vu/bao-tri"
    assert footer.get_by_role("link", name="Cho thuê thiết bị").get_attribute("href") == "#/dich-vu/thue-thiet-bi"
    assert footer.get_by_role("link", name="Thi công mạng").get_attribute("href") == "#/dich-vu/thi-cong"
    assert footer.get_by_role("link", name="Sửa chữa tận nơi").get_attribute("href") == "#/dich-vu/sua-chua"
    assert footer.get_by_role("link", name="Câu hỏi thường gặp").get_attribute("href") == "#/tin-tuc/chi-tiet"
    footer.get_by_role("link", name="Câu hỏi thường gặp").click()
    page.wait_for_url("**#/tin-tuc/chi-tiet")

    # Contact map is no longer washed out by the former 60-80% white overlay.
    page.goto("http://127.0.0.1:5173/#/lien-he")
    page.wait_for_load_state("networkidle")
    assert page.locator(".page-contact main > section:first-child > img").get_attribute("src") == "/assets/contact-map-detailed.png"
    map_overlay = page.locator(".page-contact main > section:first-child > div.absolute.inset-0")
    assert float(map_overlay.evaluate("node => getComputedStyle(node).opacity")) <= 0.16
    map_filter = page.locator(".page-contact main > section:first-child > img").evaluate("node => getComputedStyle(node).filter")
    assert "contrast" in map_filter and "saturate" in map_filter

    assert errors == [], f"Console errors: {errors}"
    print("requested_flows_test: passed")
    browser.close()
