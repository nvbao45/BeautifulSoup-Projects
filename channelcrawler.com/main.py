from bs4 import BeautifulSoup
from grpc import channel_ready_future

import requests
import csv

base_url = "https://channelcrawler.com/eng/results2/278463/page:"
csv_header = [
    "Channel Name",
    "Category",
    "Channel Link",
    "Subscribers",
    "Total View",
    "Total Video",
    "Lastest Video"
]

with open("data.csv", "w", newline='', encoding="utf-8") as csvfile:
    csv_writer = csv.DictWriter(csvfile, fieldnames=csv_header)
    csv_writer.writeheader()


for i in range(1, 16):
    res = requests.get(base_url + str(i))
    soup = BeautifulSoup(res.text, 'html.parser')

    channels = soup.select('.channel.col-xs-12')
    for channel in channels:
        channel_link = channel.select_one('h4 a')['href']
        channel_name = channel.select_one('h4 a').text
        channel_category = channel.select_one('small').text
        channel_detail = channel.select_one("p small").text

        csv_row = {
            csv_header[0]: channel_name,
            csv_header[1]: channel_category,
            csv_header[2]: channel_link,
            csv_header[3]: channel_detail.split('\n')[1].strip(),
            csv_header[4]: channel_detail.split('\n')[2].strip(),
            csv_header[5]: channel_detail.split('\n')[3].strip(),
            csv_header[6]: channel_detail.split('\n')[4].strip()
        }
        with open("data.csv", "a", newline='', encoding="utf-8") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=csv_header)
            csv_writer.writerow(csv_row)
