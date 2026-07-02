import requests
from bs4 import BeautifulSoup

url = "https://www.shl.com/solutions/products/product-catalog/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# saare script tags dekho jinme id ho
scripts = soup.find_all("script", id=True)
for s in scripts:
    print(s.get("id"))