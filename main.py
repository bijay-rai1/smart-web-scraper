import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://daraz.com.np"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = soup.find_all("h2")

data = []
for title in titles:
    data.append(title.text.strip())

df = pd.DataFrame(data, columns=["Title"])
df.to_csv("output.csv", index=False)

print("Scraping completed successfully!")
