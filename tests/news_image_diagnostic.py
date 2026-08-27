import json
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    failed_requests = []
    failed_responses = []
    page.on("requestfailed", lambda request: failed_requests.append({
        "url": request.url,
        "error": request.failure,
    }) if request.resource_type == "image" else None)
    page.on("response", lambda response: failed_responses.append({
        "url": response.url,
        "status": response.status,
    }) if response.request.resource_type == "image" and response.status >= 400 else None)

    page.goto("http://127.0.0.1:5173/#/tin-tuc")
    page.wait_for_load_state("networkidle")
    images = page.locator(".page-news img").evaluate_all(
        """images => images.map((image, index) => ({
          index,
          alt: image.alt || image.dataset.alt || '',
          src: image.currentSrc || image.src,
          complete: image.complete,
          naturalWidth: image.naturalWidth,
          naturalHeight: image.naturalHeight,
        }))"""
    )
    hero_background = page.locator(".page-news > header").evaluate(
        "node => getComputedStyle(node).backgroundImage"
    )
    print(json.dumps({
        "images": images,
        "heroBackground": hero_background,
        "failedRequests": failed_requests,
        "failedResponses": failed_responses,
    }, ensure_ascii=False))
    browser.close()
