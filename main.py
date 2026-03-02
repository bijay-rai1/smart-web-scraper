from playwright.sync_api import sync_playwright
import pandas as pd
from urllib.parse import urljoin, urlparse

# Configuration
BASE_URL = "https://globalforcefc.github.io"
DOMAIN = urlparse(BASE_URL).netloc
data = []
visited = set()
queue = [BASE_URL]

def scrape_page(page, url):
    if url in visited:
        return
    visited.add(url)
    
    print(f"Scraping: {url}")
    try:
        page.goto(url, timeout=60000)
        page.wait_for_load_state("networkidle")
        
        # --- Extraction Logic ---
        # (Same as your original logic, adding 'URL' for clarity)
        
        # 1. Title
        data.append({"URL": url, "Type": "Title", "Content": page.title(), "Attribute": "", "Link": ""})

        # 2. Headings
        for tag in page.query_selector_all("h1, h2, h3"):
            data.append({"URL": url, "Type": "Heading", "Content": tag.inner_text(), "Attribute": tag.evaluate("el => el.tagName"), "Link": ""})

        # 3. Paragraphs
        for p_tag in page.query_selector_all("p"):
            text = p_tag.inner_text().strip()
            if text:
                data.append({"URL": url, "Type": "Paragraph", "Content": text, "Attribute": "", "Link": ""})

        # 4. Links (The Crawler Engine)
        links = page.query_selector_all("a")
        for link in links:
            href = link.get_attribute("href")
            if not href:
                continue
            
            # Normalize the URL
            full_url = urljoin(url, href)
            parsed_url = urlparse(full_url)

            # Only follow links within the same domain
            if parsed_url.netloc == DOMAIN and full_url not in visited:
                if full_url not in queue:
                    queue.append(full_url)

            # Store the link data as usual
            data.append({"URL": url, "Type": "Link", "Content": link.inner_text(), "Attribute": "", "Link": full_url})

    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Process the queue until empty
    while queue:
        current_url = queue.pop(0)
        scrape_page(page, current_url)

    browser.close()

# Save Data
df = pd.DataFrame(data)
df.to_csv("full_site_output.csv", index=False)
print(f"Crawl finished! Visited {len(visited)} pages.")
