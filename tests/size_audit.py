import json
from playwright.sync_api import sync_playwright


ROUTES = [
    "/",
    "/dich-vu/thue-thiet-bi",
    "/dich-vu/bao-tri",
    "/dich-vu/sua-chua",
    "/dich-vu/thi-cong",
    "/dich-vu/chi-tiet",
    "/tin-tuc",
    "/tin-tuc/chi-tiet",
    "/tuyen-dung",
    "/lien-he",
]


SCRIPT = """() => {
  const visible = element => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const text = element => element.innerText.replace(/\\s+/g, ' ').trim();
  const describe = element => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return {
      text: text(element).slice(0, 90),
      font: Math.round(parseFloat(style.fontSize)),
      line: Math.round(parseFloat(style.lineHeight)),
      width: Math.round(rect.width),
      height: Math.round(rect.height),
    };
  };
  const headings = [...document.querySelectorAll('.legacy-page h1, .legacy-page h2')].filter(visible).map(describe);
  const buttons = [...document.querySelectorAll('button, a.bg-primary-container, a.btn-primary')].filter(visible).map(describe);
  const images = [...document.querySelectorAll('.legacy-page img')].filter(visible).map(image => ({
    alt: image.alt || image.dataset.alt || '',
    width: Math.round(image.getBoundingClientRect().width),
    height: Math.round(image.getBoundingClientRect().height),
  }));
  return {
    overflow: document.body.scrollWidth - document.documentElement.clientWidth,
    headings: headings.sort((a, b) => b.font - a.font).slice(0, 8),
    buttons: buttons.sort((a, b) => b.height - a.height || b.font - a.font).slice(0, 8),
    images: images.sort((a, b) => b.height - a.height).slice(0, 4),
  };
}"""


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    result = {}
    for viewport, size in (
        ("desktop", {"width": 1440, "height": 900}),
        ("mobile", {"width": 390, "height": 844}),
    ):
        page = browser.new_page(viewport=size)
        result[viewport] = {}
        for route in ROUTES:
            page.goto(f"http://127.0.0.1:5173/#{route}")
            page.wait_for_load_state("networkidle")
            result[viewport][route] = page.evaluate(SCRIPT)
        page.close()
    print(json.dumps(result, ensure_ascii=False))
    browser.close()
