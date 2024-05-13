from typing_extensions import Required
from bs4 import BeautifulSoup

import requests
import sys

def make_link(keyword):
    url = f"https://www.made-in-china.com/productdirectory.do?word={keyword}&file=&searchType=0&subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0&isOpenCorrection=1&org=top"
    return url

url = make_link(sys.argv[1])
headers = {
    'User-Agent': 'Mozilla/5.0',
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')
prod_list = soup.select(".prod-list div.list-node")
for prod in prod_list:
    image = prod.select_one("img")['src']
    title = prod.select_one(".product-name a").text

    print(image)
    print(title.strip())
    print("\n\n")