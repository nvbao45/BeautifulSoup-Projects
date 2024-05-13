import re
import imgkit
import csv

from bs4 import BeautifulSoup
import urllib.request
import urllib.request, urllib.error, urllib.parse


imgkit_config = imgkit.config(
    wkhtmltoimage="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"
)
base_url = '''
    https://classifieds.mcclatchy.com/marketplace/biloxi/search/query?categoryId=5&searchProfile=notices&source=biloxi&page=1&size=100&view=list&showExtended=false&startRange=&keywords=&firstDate=07%2F27%2F2022&lastDate=07%2F27%2F2022&ordering=BY_DATE_DEC
'''

with open('dataset.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'content', 'image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

def get(url):
    request = urllib.request.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0")
    response = urllib.request.urlopen(request)
    webContent = response.read().decode('UTF-8')
    return webContent

soup = BeautifulSoup(get(base_url), 'html.parser')

results_frame = soup.select('.description.media-body.linkify')
for result in results_frame:
    viewmore_link = result.a['href']
    content_soup = BeautifulSoup(get(viewmore_link), 'html.parser')
    content = content_soup.select('.panel-body p.linkify')[0]
    id = content_soup.select('.sr_ad_frame')[0]['id']

    imgkit.from_url(viewmore_link, f'{id}.jpg', config=imgkit_config)
    print(content.string)
    with open('dataset.csv', 'a', newline='') as csvfile:
        fieldnames = ['id', 'content', 'image']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(
            {
                'id': id, 
                'content': content.string,
                'image': str(id) + '.jpg'
            }
        )