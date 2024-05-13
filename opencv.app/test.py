from asyncore import write
import csv
from traceback import print_last
import requests
import re
import urllib.request
import urllib.request, urllib.error, urllib.parse

from bs4 import BeautifulSoup


APPEND_MODE     = False
LAST_ROW        = 0
RECONNECT_MAX   = 3

base_url = "https://www.openvc.app/"
all_fund = base_url + "all-funds"

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
            pass
    soup.clear()

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


# web_content = get(all_fund)
# soup = BeautifulSoup(web_content, 'html.parser')

# count = 0
# for a in soup.select('a'):
#     link = a.get("href")

link = "https://www.openvc.app/fund/Highline%20Beta"
if link != None:
    profile = get_profile(link)
    print(profile)