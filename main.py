from playwright.sync_api import sync_playwright
import pandas as pd

data = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.daraz.com.np", timeout=60000)
    page.wait_for_load_state("networkidle")

    # ======================
    # Page Title
    # ======================
    data.append({
        "Type": "Title",
        "Content": page.title(),
        "Attribute": "",
        "Link": ""
    })

    # ======================
    # Meta Tags
    # ======================
    metas = page.query_selector_all("meta")
    for meta in metas:
        name = meta.get_attribute("name") or meta.get_attribute("property")
        content = meta.get_attribute("content")
        if name and content:
            data.append({
                "Type": "Meta",
                "Content": content,
                "Attribute": name,
                "Link": ""
            })

    # ======================
    # Headings
    # ======================
    for tag in page.query_selector_all("h1, h2, h3, h4, h5, h6"):
        data.append({
            "Type": "Heading",
            "Content": tag.inner_text(),
            "Attribute": tag.evaluate("el => el.tagName"),
            "Link": ""
        })

    # ======================
    # Paragraphs
    # ======================
    for p_tag in page.query_selector_all("p"):
        text = p_tag.inner_text().strip()
        if text:
            data.append({
                "Type": "Paragraph",
                "Content": text,
                "Attribute": "",
                "Link": ""
            })

    # ======================
    # Lists
    # ======================
    for li in page.query_selector_all("li"):
        text = li.inner_text().strip()
        if text:
            data.append({
                "Type": "List Item",
                "Content": text,
                "Attribute": "",
                "Link": ""
            })

    # ======================
    # Tables
    # ======================
    tables = page.query_selector_all("table")
    for table in tables:
        rows = table.query_selector_all("tr")
        for row in rows:
            cols = row.query_selector_all("th, td")
            row_data = [col.inner_text().strip() for col in cols]
            if row_data:
                data.append({
                    "Type": "Table Row",
                    "Content": " | ".join(row_data),
                    "Attribute": "",
                    "Link": ""
                })

    # ======================
    # Links
    # ======================
    for link in page.query_selector_all("a"):
        data.append({
            "Type": "Link",
            "Content": link.inner_text(),
            "Attribute": "",
            "Link": link.get_attribute("href")
        })

    # ======================
    # Images
    # ======================
    for img in page.query_selector_all("img"):
        data.append({
            "Type": "Image",
            "Content": img.get_attribute("alt"),
            "Attribute": "",
            "Link": img.get_attribute("src")
        })

    # ======================
    # Save Full HTML
    # ======================
    html_content = page.content()
    with open("full_page.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    browser.close()

# Save CSV
df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)

print("Full website scraping completed successfully!")
