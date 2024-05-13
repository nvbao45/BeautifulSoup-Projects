from asyncore import write
import csv
from traceback import print_last
import requests
import re
import urllib.request
import urllib.request, urllib.error, urllib.parse

from bs4 import BeautifulSoup

old_csv_file = "smm.csv"
new_csv_file = "smm-linkedin.csv"

csvfile = open(old_csv_file, encoding="utf-8")
csvreader = csv.reader(csvfile)
header = next(csvreader)

with open(new_csv_file, "w", newline='', encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()

def get(url):
    retry_counter = 0
    webcontent = ""

    while retry_counter < 5:
        try:
            headers = {
            "User-Agent": "Mozilla/5.0"
            }
            res = requests.get(url, headers=headers, verify=False)
            webcontent = res.text
            res.close()
            break
        except:
            retry_counter += 1

    return webcontent


def get_linkedin_in_website(web_url):
    soup = BeautifulSoup(get(web_url), "html.parser")
    for anchor in soup.find_all('a'):
        try:
            url = anchor['href']
            if 'linkedin.com' in url:
                return url
        except:
            pass
    soup.clear()
    return ""

count = 0
update_count = 0
for row in csvreader:
    url = row[18]
    linkedin = row[13]
    if linkedin == "" and url != "":
        linkedin = get_linkedin_in_website(url)
        if linkedin != "":
            update_count += 1
    
    count += 1
    csv_row = {
        header[0]: row[0],
        header[1]: row[1],
        header[2]: row[2],
        header[3]: row[3],
        header[4]: row[4],
        header[5]: row[5],
        header[6]: row[6],
        header[7]: row[7],
        header[8]: row[8],
        header[9]: row[9],
        header[10]: row[10],
        header[11]: row[11],
        header[12]: row[12],
        header[13]: linkedin,
        header[14]: row[14],
        header[15]: row[15],
        header[16]: row[16],
        header[17]: row[17],
        header[18]: row[18],
        header[19]: row[19],
    }

    print(f"Work on row: {count}")
    print(f"Website url: {url}")
    print(f"Linkedin url: {linkedin}")
    print(f"No. row has updated: {update_count}\n")
    with open(new_csv_file, "a", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writerow(csv_row) 