import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://worldmonitor.app/?lat=28.7021&lon=37.0223&zoom=3.95&view=global&timeRange=7d&layers=conflicts%2Cbases%2Chotspots%2Cnuclear%2Csanctions%2Cweather%2Ceconomic%2Cwaterways%2Coutages%2Cmilitary%2Cnatural%2CiranAttacks"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

data = []

# Extract page title
page_title = soup.title.string if soup.title else "No Title"

# Extract all headings
for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
    data.append({
        "Type": "Heading",
        "Content": tag.get_text(strip=True),
        "Link": "",
        "Image": ""
    })

# Extract all links
for link in soup.find_all("a"):
    data.append({
        "Type": "Link",
        "Content": link.get_text(strip=True),
        "Link": link.get("href"),
        "Image": ""
    })

# Extract all images
for img in soup.find_all("img"):
    data.append({
        "Type": "Image",
        "Content": img.get("alt"),
        "Link": "",
        "Image": img.get("src")
    })

df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)

print("Scraping completed successfully!")
