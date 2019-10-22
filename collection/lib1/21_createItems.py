import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

rows = []
rows.append(["id", "cn", "title", "vol", "pub", "extent", "memo"])

url = "http://www.tbcas.jp/ja/lib/lib1/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
trs = soup.find_all("tr")
for tr in trs:
    print(tr)
    tds = tr.find_all("td")
    if len(tds) == 0:
        continue

    cn = tr.find("th").text
    title = tds[0].text
    vol = tds[1].text
    pub = tds[2].text
    extent = tds[3].text
    memo = tds[4].text

    aas = tds[5].find_all("a")

    for a in aas:
        href = a.get("href")


        if "lib5" in href:
            id = href.split("/data/")[1].replace("/", "-")
            rows.append([id, cn, title, vol, pub, extent, memo])

import csv

f = open('data/items.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

            
