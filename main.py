from playwright.sync_api import sync_playwright
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://worldmonitor.app")

    page.wait_for_timeout(5000)

    title = page.title()
    print("Page Title:", title)

    content = page.content()

    df = pd.DataFrame([{"Title": title}])
    df.to_csv("output.csv", index=False)

    browser.close()

print("Scraping completed successfully!")
