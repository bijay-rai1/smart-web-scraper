from playwright.sync_api import sync_playwright
import pandas as pd

data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Set realistic user agent
    page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    })

    page.goto("https://globalforcefc.github.io", timeout=60000)
    page.wait_for_load_state("networkidle")

    # Page Title
    title = page.title()
    data.append({
        "Type": "Title",
        "Content": title,
        "Link": "",
        "Image": ""
    })

    # Extract Headings
    headings = page.query_selector_all("h1, h2, h3, h4, h5, h6")
    for h in headings:
        data.append({
            "Type": "Heading",
            "Content": h.inner_text(),
            "Link": "",
            "Image": ""
        })

    # Extract Links
    links = page.query_selector_all("a")
    for link in links:
        data.append({
            "Type": "Link",
            "Content": link.inner_text(),
            "Link": link.get_attribute("href"),
            "Image": ""
        })

    # Extract Images
    images = page.query_selector_all("img")
    for img in images:
        data.append({
            "Type": "Image",
            "Content": img.get_attribute("alt"),
            "Link": "",
            "Image": img.get_attribute("src")
        })

    # Extract All Visible Text
    body_text = page.inner_text("body")
    data.append({
        "Type": "Full Page Text",
        "Content": body_text,
        "Link": "",
        "Image": ""
    })

    browser.close()

df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)

print("Scraping completed successfully!")
