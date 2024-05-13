import requests

from bs4 import BeautifulSoup

base_url = "https://vn.indeed.com/cmp/Puma/reviews?fcountry=ALL"

res = requests.get(base_url)
soup = BeautifulSoup(res.text, 'html.parser')

reviews = soup.find_all("div", {"data-tn-entitytype": "reviewId"})

for review in reviews:
    star = review.select_one('meta')['content']
    content = review.find('div', {"data-tn-component": "reviewDescription"}).text

    print(f"Start: {star}")
    print(f"Review: {content}\n\n")