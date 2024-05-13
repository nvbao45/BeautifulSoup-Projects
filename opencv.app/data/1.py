from asyncore import write
import csv
from traceback import print_last
import requests
import re
import urllib.request
import urllib.request, urllib.error, urllib.parse

from bs4 import BeautifulSoup

APPEND_MODE     = True
LAST_ROW        = 704
RECONNECT_MAX   = 3


old_csv_file = "1.csv"
new_csv_file = "1-linkedin.csv"

csvfile = open(old_csv_file, encoding="utf-8")
csvreader = csv.reader(csvfile)
header = next(csvreader)

if not APPEND_MODE:
    with open(new_csv_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

def get(url):
    retry_counter = 0
    webcontent = ""

    while retry_counter < RECONNECT_MAX:
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
try:
    for row in csvreader:
        count += 1
        if APPEND_MODE and count < LAST_ROW:
            continue
        url = row[1]
        linkedin = row[2]

        print(f"Work on row: {count}")
        print(f"Website url: {url}")

        if url != "" and linkedin == "":
            linkedin = get_linkedin_in_website(url)
            if linkedin != "":
                update_count += 1
        
        csv_row = {
            header[0]: row[0],
            header[1]: row[1],
            header[2]: linkedin,
            header[3]: row[3],
            header[4]: row[4],
            header[5]: row[5],
            header[6]: row[6],
            header[7]: row[7],
            header[8]: row[8],
            header[9]: row[9],
        }

        print(f"Linkedin url: {linkedin}")
        print(f"No. row has updated: {update_count}\n")
        with open(new_csv_file, "a", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(csv_row) 
except:
    print(f"Error at row {count}")
    pass