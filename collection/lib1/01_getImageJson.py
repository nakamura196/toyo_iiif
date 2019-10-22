import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

books = ["MCJB01249"]

url = "http://www.tbcas.jp/ja/lib/lib1/"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")
aas = soup.find_all("a")
for a in aas:
    href = a.get("href")

    if "lib5" in href:
        books.append(href.split("/data/")[1])

for i in range(len(books)):

    print(str(i+1)+"/"+str(len(books)))

    book = books[i]

    loop_flg = True  

    # print(book)

    page = 1

    while loop_flg:

        path  = "tmp/"+book.replace("/", "-")+"_"+str(page).zfill(3)+".json"

        print(str(book)+"_"+str(page))

        if not os.path.exists(path):

            '''
            url = "http://124.33.215.236/research/atoinga/"+str(book).zfill(3)+"/pageindices/index"+str(page)+".html"

            print(url)

            sleep(1)

            try:
                html = urllib.request.urlopen(url)
            except:
                print(url)
                loop_flg = False
                continue

            # htmlをBeautifulSoupで扱う
            soup = BeautifulSoup(html, "html.parser")

            text = soup.find(id="searchText")

            '''

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

       
