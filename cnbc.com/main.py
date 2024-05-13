from bs4 import BeautifulSoup 

import requests

base_url = "https://www.cnbc.com/world/?region=world"


lastestnews = ''

while True:
    res = requests.get(base_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    lastestnews_list = soup.select_one('ul.LatestNews-list > li')
    lastestnews_timestamp = lastestnews_list.select_one(".LatestNews-timestamp").text
    lastestnews_headline = lastestnews_list.select_one(".LatestNews-headline").text
    if lastestnews != lastestnews_headline:
        lastestnews = lastestnews_headline
        print(lastestnews_timestamp)
        print(lastestnews)
        #send notify
    else:
        print("Waiting for news ...", end="\r")
    