import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

import requests
import shutil

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def dwn(url, arr):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    
    img = soup.find("img")

    src = "http://124.33.215.236/gazou/2009/" + img.get("src")
    arr.append(src)


url = "http://124.33.215.236/gazou/index_img_iwasakizenponsasyoku.php"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

aas = soup.find_all("a")

urls = []

for a in aas:
    href = a.get("href")

    # print(href)
    urls.append(href)

for url in sorted(urls):
    # print(url)

    if "2009" in url:
        url = "http://124.33.215.236/gazou/"+url.replace("./", "")
        print(url)

        id = url.split("TGName=")[1].split("&")[0]
        

        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("strong").text.strip()

        arr = []
        result = {
            "id": id,
            "title": title,
            "url": url,
            "arr": arr
        }

        dwn(url, arr)

        aas = soup.find_all("a")

        for a in aas:
            href = a.get("href")
            if "gazo2009_read.php" in href:
                url = "http://124.33.215.236/gazou/2009/" + href
                dwn(url, arr)

        
        with open("tmp/"+id+".json", 'w') as outfile:
            json.dump(result, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))


'''
aas = soup.find_all("a")
for a in aas:
    href = a.get("href")

    if "lib5" in href:
        books.append(href.split("/data/")[1])

for i in range(0, len(books)):

    sleep(1)

    print(str(i+1)+"/"+str(len(books)))

    book = books[i]

    loop_flg = True  

    # print(book)

    page = 1

    while loop_flg:

        path  = "tmp/"+book.replace("/", "-")+"_"+str(page).zfill(3)+".json"

        print(str(book)+"_"+str(page))

        if not os.path.exists(path):

            

            text = None

            page_str = str(page).zfill(4)

            try:

                src = "http://www.tbcas.jp/ja/lib/lib5/data/"+book+"/files/assets/flash/pages/page"+page_str+"_l.jpg"
                # print(src)

                image = Image.open(urllib.request.urlopen(src))
                width, height = image.size

                thumb = "http://www.tbcas.jp/ja/lib/lib5/data/"+book+"/files/assets/flash/pages/page"+page_str+"_s.png"
            except:
                src = "http://design-ec.com/d/e_others_50/l_e_others_500.png"
                width = "600"
                height = "600"
                thumb = "http://design-ec.com/d/e_others_50/l_e_others_500.png"

                loop_flg = False
                continue

            obj = {
                "original": src,
                "thumbnail": thumb,
                "book": book,
                "page": page,
                "width": width,
                "height": height
            }

            if text != None and text != "":
                obj["text"] = text.text.strip()

            with open(path, 'w') as outfile:
                json.dump(obj, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        
        page += 1

'''
       
