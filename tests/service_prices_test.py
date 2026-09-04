from playwright.sync_api import sync_playwright


EXPECTED = {
    "/dich-vu/thue-thiet-bi": [
        "500.000\u0111", "500.000\u0111", "800.000\u0111", "200.000\u0111",
        "100.000\u0111", "300.000\u0111", "Li\u00ean h\u1ec7 t\u01b0 v\u1ea5n", "200.000\u0111",
        "300.000\u0111", "300.000\u0111",
    ],
    "/dich-vu/bao-tri": [
        "80.000\u0111", "100.000\u0111", "300.000\u0111", "100.000\u0111", "300.000\u0111",
    ],
    "/dich-vu/sua-chua": ["150.000\u0111", "150.000\u0111"],
    "/dich-vu/thi-cong": ["500.000\u0111", "100.000\u0111", "100.000\u0111", "100.000\u0111"],
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for viewport in ({"width": 390, "height": 844}, {"width": 1440, "height": 1000}):
        page = browser.new_page(viewport=viewport)
        console_errors = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)

        for route, expected_amounts in EXPECTED.items():
            page.goto(f"http://localhost:5173/#{route}")
            page.wait_for_load_state("networkidle")

            summaries = page.locator(".service-price-summary")
            assert summaries.count() == len(expected_amounts), route
            assert summaries.locator(".service-price-label").all_text_contents() == [
                "Gi\u00e1 d\u1ecbch v\u1ee5"
            ] * len(expected_amounts), route
            assert summaries.locator(".service-price-amount").all_inner_texts() == expected_amounts, route

            numeric_price_count = sum(amount != "Li\u00ean h\u1ec7 t\u01b0 v\u1ea5n" for amount in expected_amounts)
            assert summaries.locator(".service-price-from").count() == numeric_price_count, route
            assert summaries.evaluate_all(
                """nodes => nodes.every(node => {
                    const style = getComputedStyle(node)
                    const amount = node.querySelector('.service-price-amount')
                    return node.scrollWidth <= node.clientWidth
                        && style.borderRadius === '0px'
                        && style.backgroundColor === 'rgba(0, 0, 0, 0)'
                        && amount
                        && parseFloat(getComputedStyle(amount).fontSize) >= 27
                })"""
            ), route

        assert not console_errors, console_errors
        page.close()

    browser.close()

print("Verified the approved price design on 21 responsive service cards.")
