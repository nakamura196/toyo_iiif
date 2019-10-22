import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image

for book in range(1, 13):

    loop_flg = True  

    print(book)

    page = 1

    while loop_flg:

        path  = "tmp/"+str(book).zfill(3)+"_"+str(page).zfill(3)+".json"

        print(page)

        if not os.path.exists(path):

            url = "http://124.33.215.236/research/atoinga/"+str(book).zfill(3)+"/pageindices/index"+str(page)+".html"

            sleep(1)

            try:
                html = urllib.request.urlopen(url)
            except:
                loop_flg = False
                continue

            # htmlをBeautifulSoupで扱う
            soup = BeautifulSoup(html, "html.parser")

            text = soup.find(id="searchText")
            if text:
                print(text.text.strip())

            src = "http://124.33.215.236/research/atoinga/001/page"+str(page)+"/x1.jpg"

            image = Image.open(urllib.request.urlopen(src))
            width, height = image.size

            thumb = "http://124.33.215.236/research/atoinga/001/page"+str(page)+"/thumbnail.jpg"

            obj = {
                "original": src,
                "thumbnail": thumb,
                "book": "001",
                "page": page,
                "width": width,
                "height": height
            }

            if text != "":
                obj["text"] = text.text.strip()

            with open(path, 'w') as outfile:
                json.dump(obj, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        
        page += 1

       
