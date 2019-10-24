import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

import requests
import shutil
import urllib.parse

def download_img(url, file_name):
    print("img="+url)
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def dwn(url, arr):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    
    img = soup.find("img")

    src = urllib.parse.urljoin(url, img.get("src"))

    # opath = src.replace("http://124.33.215.236/", "../../")

    arr.append(src)


url = "http://124.33.215.236/gazou/index_img.php?tg=J1"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

aas = soup.find_all("a")

urls = []

for a in aas:
    href = urllib.parse.urljoin(url, a.get("href"))
    urls.append(href)

for url0 in sorted(urls):

    if "201511" in url0:
        print("url0="+url0)

        id = url0.split("lstdir=")[1].split("&")[0]

        try:
            html = requests.get(url0).text
        except Exception as e:
            print(e)
            continue
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1").text.strip()

        arr = []
        result = {
            "id": id,
            "title": title,
            "url": url,
            "arr": arr
        }

        dwn(url0, arr)

        aas = soup.find_all("a")

        for a in aas:
            href = urllib.parse.urljoin(url0, a.get("href"))
            if "201511.php" in href:
                dwn(href, arr)

        with open("tmp/"+id+".json", 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))