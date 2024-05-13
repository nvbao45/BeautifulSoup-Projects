from asyncore import write
from bs4 import BeautifulSoup

import threading
import requests
import json
import csv

from sqlalchemy import null

base_url = "https://www.smm-hamburg.com/en/programme-exhibitors/exhibitors-products/exhibitor-directory"
detail_url = "https://www.smm-hamburg.com/en/platform"

csv_header = [
    "Id", 
    "Name", 
    "Type", 
    "Profile", 
    "Image", 
    "Location",
    "CorpStreet",
    "ZipCode",
    "City",
    "Country",
    "Tel",
    "Fax",
    "Email",
    "LinkedIn",
    "Facebook",
    "Instagram",
    "Twitter",
    "Xing",
    "Web",
    "Product"
    ]
with open("data.csv", 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_header)
    writer.writeheader()


payload = {
    "no_cache": 1,
    "tx_hmcplatform_api[action]": "search",
    "tx_hmcplatform_api[controller]": "DiscoverApi",
    "type": "1603899437",
    "tx_hmcplatform_api[term]": "",
    "tx_hmcplatform_api[expoCode]": "SM22",
    "tx_hmcplatform_api[objectType]": "CORPORATION",
    "tx_hmcplatform_api[startsWith]": "",
    "tx_hmcplatform_api[sortOrder]": "ASC",
    "tx_hmcplatform_api[page]": 0,
    "tx_hmcplatform_api[limit]": 30
}

detail_payload = {
    "tx_hmcplatform_api[action]": "show",
    "tx_hmcplatform_api[controller]": "DiscoverApi",
    "tx_hmcplatform_api[expoCode]": "SM22",
    "tx_hmcplatform_api[id]": 57478,
    "tx_hmcplatform_api[type]": "corporation",
    "type": "1603899437",
}

count = 0
for i in range (0, 65):
    try:
        payload["tx_hmcplatform_api[page]"] = i
        res = requests.get(base_url, params=payload)
        data = json.loads(res.text)
        for item in data['items']:
            try:
                print(f"Get detail company id {item['id']}")
                print(f"Get {count} company\n")

                detail_payload['tx_hmcplatform_api[id]'] = item['id']
                detail_payload['tx_hmcplatform_api[type]'] = item['type']

                detail_res = requests.get(detail_url, params=detail_payload)
                detail_data = json.loads(detail_res.text)

                detail = detail_data['item']
                image = ""
                if detail['image'] != None:
                    for img in detail['image']:
                        image += img['url'] + "\r\n"

                product = ""
                if detail['product'] != None:
                    for pro in detail['product']:
                        product += pro['prodTitle'] + "\r\n"

                csv_row = {
                    "Id": detail['id'],
                    "Name": detail['title'],
                    "Type": detail['type'],
                    "Profile": detail['corpProfile'],
                    "Image": image,
                    "Location": "Hall " + detail['stand'][0]['expoHall'] + ", Stand " + detail['stand'][0]['standNo'],
                    "CorpStreet": detail['corpStreet'],
                    "ZipCode": detail['corpZip'],
                    "City": detail['corpCity'],
                    "Country": detail['corpCountry'],
                    "Tel": detail['corpTel'],
                    "Fax": detail['corpFax'],
                    "Email": detail['corpEmail'],
                    "LinkedIn": detail['corpSocialLinkedin'],
                    "Facebook": detail['corpSocialFacebook'],
                    "Instagram": detail['corpSocialInstagram'],
                    "Twitter": detail['corpSocialTwitter'],
                    "Xing": detail['corpSocialXing'],
                    "Web": detail['corpWeb'],
                    "Product": product
                }
                with open("data.csv", 'a', newline='', encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=csv_header)
                    writer.writerow(csv_row)

                count += 1
            except:
                pass
    except:
        pass