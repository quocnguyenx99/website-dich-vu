from playwright.sync_api import sync_playwright


EXPECTED_IMAGES = {
    "/dich-vu/thue-thiet-bi": ["it-equipment-rental-hero.png"],
    "/dich-vu/thi-cong": [
        "server-configuration-service.png",
        "office-security-camera-monitoring.png",
        "camera-removal-relocation-service.png",
        "camera-installation-service.png",
    ],
}


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()

    for route, expected_images in EXPECTED_IMAGES.items():
        page.goto(f"http://localhost:5173/#{route}")
        page.wait_for_load_state("networkidle")
        image_sources = page.locator("img").evaluate_all("images => images.map(image => image.getAttribute('src'))")
        for image in expected_images:
            assert any(source and source.endswith(image) for source in image_sources), f"{route} does not use {image}"

    browser.close()

print("Verified generated service images on rental and deployment pages.")
