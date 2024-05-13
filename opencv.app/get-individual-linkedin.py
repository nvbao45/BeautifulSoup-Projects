from asyncore import write
import csv
from traceback import print_last
import requests
import re
import urllib.request
import urllib.request, urllib.error, urllib.parse

from bs4 import BeautifulSoup

APPEND_MODE     = True
LAST_ROW        = 4511
RECONNECT_MAX   = 3

old_csv_file = "openvc-linkedin.csv"
new_csv_file = "openvc-linkedin-new.csv"

base_url = "https://www.openvc.app/fund/"
base_profile_url = "https://www.openvc.app/"

csvfile = open(old_csv_file, encoding='utf-8')
csvreader = csv.reader(csvfile)
next(csvreader)

header = [
    "Investor name","Website","Linkedin","Individual LinkedIn",
    "Global HQ","Countries of investment","Stage of investment",
    "Investment thesis","Investor type","First cheque minimum","First cheque maximum"
]

if not APPEND_MODE:
    with open(new_csv_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

def get(url):
    retry_counter = 0
    webcontent    = ""
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
            return ""
    soup.clear()
    return ""

def get_profile(web_url):
    web_content = get(web_url)
    soup = BeautifulSoup(web_content, 'html.parser')
    profiles = []
    try:
        profile_table = soup.select_one("#teamCont table").select('tr')
        for profile in profile_table:
            link = profile.select_one("a")['href']
            profiles.append(link)
        return profiles
    except:
        return ""



count            = 0
update_count     = 0
individual_count = 0
try:
    for row in csvreader:
        count += 1
        if APPEND_MODE and count < LAST_ROW:
            continue
        
        investor_name       = row[0]
        linkedin            = row[2]
        url                 = base_url + investor_name
        individual_linkedin = ''
        print(f"Go to: {url}")

        team_profiles       = get_profile(url)
        for profile in team_profiles:
            profile_url = base_profile_url + profile
            print("Get linkedin in profile:")
            print(f"\t{profile_url}")
            individual_linkedin = get_linkedin_in_website(profile_url) + "\r\n"
            individual_count += 1
        
        print(f"Work on row: {count}")
        print(f"Investor name: {investor_name}")
        print(f"Individual linkedin: {individual_linkedin}")
        print(f"Linkedin url: {linkedin}")
        print(f"Individual count: {individual_count}\n")       

        csv_row = {
            header[0]: row[0],
            header[1]: row[1],
            header[2]: row[2],
            header[3]: individual_linkedin,
            header[4]: row[3],
            header[5]: row[4],
            header[6]: row[5],
            header[7]: row[6],
            header[8]: row[7],
            header[9]: row[8],
        }

        with open(new_csv_file, "a", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=header)
            writer.writerow(csv_row) 
except Exception as e:
    print(f"Error at row {count}")
    print(e)
    pass