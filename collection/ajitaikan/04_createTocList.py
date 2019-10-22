import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

rows = []
rows.append(["ID", "Page", "Toc"])

for book in range(1, 13):

    loop_flg = True  

    print(book)

    page = 1

    url = "http://124.33.215.236/research/atoinga/"+str(book).zfill(3)+"/index.html"

    html = urllib.request.urlopen(url)

    # htmlをBeautifulSoupで扱う
    soup = BeautifulSoup(html, "html.parser")

    lis = soup.find_all("li")
    for li in lis:
        page = int(li.find("a").get("href").split("/index")[1].replace(".html", "")) - 1
        text = li.text

        rows.append([str(book).zfill(3), page, text])

import csv

f = open('data/toc.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
       
