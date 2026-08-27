from playwright.sync_api import sync_playwright


def font_size(locator):
    return round(float(locator.evaluate("node => getComputedStyle(node).fontSize.replace('px', '')")))


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    desktop = browser.new_page(viewport={"width": 1440, "height": 900})
    desktop.goto("http://127.0.0.1:5173/#/")
    desktop.wait_for_load_state("networkidle")
    assert font_size(desktop.get_by_role("heading", name="DANH MỤC DỊCH VỤ")) == 40
    desktop.goto("http://127.0.0.1:5173/#/lien-he")
    desktop.wait_for_load_state("networkidle")
    assert font_size(desktop.get_by_role("heading", name="Liên Hệ", exact=True)) == 36

    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    mobile.goto("http://127.0.0.1:5173/#/")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.get_by_role("heading", name="DANH MỤC DỊCH VỤ")) == 32

    mobile.goto("http://127.0.0.1:5173/#/dich-vu/thue-thiet-bi")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.get_by_role("heading", name="Dịch vụ Thuê Thiết Bị IT Chuyên Nghiệp")) == 34
    assert font_size(mobile.get_by_role("heading", name="Dịch Vụ Thuê Thiết Bị", exact=True)) == 32

    mobile.goto("http://127.0.0.1:5173/#/dich-vu/chi-tiet")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.locator(".page-service-detail h1")) == 32

    mobile.goto("http://127.0.0.1:5173/#/tin-tuc")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.get_by_role("heading", name="TIN TỨC - KIẾN THỨC")) == 34
    assert font_size(mobile.locator(".page-news article h2").first) == 24

    mobile.goto("http://127.0.0.1:5173/#/tuyen-dung")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.get_by_role("heading", name="Gia Nhập Đội Ngũ Chính Nhân Technology")) == 34
    assert font_size(mobile.get_by_role("heading", name="Chưa tìm thấy vị trí phù hợp?")) == 30

    mobile.goto("http://127.0.0.1:5173/#/lien-he")
    mobile.wait_for_load_state("networkidle")
    assert font_size(mobile.get_by_role("heading", name="Liên Hệ", exact=True)) == 30

    print("typography_test: passed")
    browser.close()
