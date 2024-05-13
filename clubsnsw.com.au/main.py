from bs4 import BeautifulSoup

import requests
import csv
import json

base_url = "https://www.clubsnsw.com.au/views/ajax?_wrapper_format=drupal_ajax"

for i in range(0, 3):
    payload = {
        "view_name": "all_clubs",
        "view_display_id": "page_1",
        "pager_element": 0,
        "page": {i}
    }
    res = requests.post(base_url, data=payload)
    json_res = json.loads(res.text)
    soup = BeautifulSoup(json_res[4]['data'], 'html.parser')
    title = soup.select_one("h2").text
    print(title)