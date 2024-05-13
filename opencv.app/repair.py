from asyncore import write
import csv
from traceback import print_last
import requests

from bs4 import BeautifulSoup

APPEND_MODE     = False
LAST_ROW        = 0
RECONNECT_MAX   = 3


old_csv_file = "openvc-linkedin-new.csv"
new_csv_file = "openvc-linkedin-new-repaired.csv"

csvfile = open(old_csv_file, encoding="utf-8")
csvreader = csv.reader(csvfile)
header = next(csvreader)

if not APPEND_MODE:
    with open(new_csv_file, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()

count = 0
update_count = 0
try:
    for row in csvreader:
        count += 1
        print(f"Working in row: {count}")
        csv_row = {
            header[0]: row[0],
            header[1]: row[1],
            header[2]: row[2],
            header[3]: row[3].replace("\r\n", "").replace("\n", "").replace("\"", ""),
            header[4]: row[4],
            header[5]: row[5],
            header[6]: row[6],
            header[7]: row[7],
            header[8]: row[8],
            header[9]: row[9],
        }
        try:
            with open(new_csv_file, "a", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=header)
                writer.writerow(csv_row) 
        except:
            pass
except Exception as e:
    print(f"Error at row {count}")
    print(e)
    pass