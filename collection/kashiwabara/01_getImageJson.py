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

        print(str(book)+"_"+str(page))

        if not os.path.exists(path):

            url = "http://www.tbcas.jp/ja/lib/lib2/"+str(book).zfill(3)+"/pageindices/index"+str(page)+".html"

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

            try:

                src = "http://www.tbcas.jp/ja/lib/lib2/"+str(book).zfill(3)+"/page"+str(page)+"/x1.jpg"
                print(src)

                image = Image.open(urllib.request.urlopen(src))
                width, height = image.size

                thumb = "http://www.tbcas.jp/ja/lib/lib2/"+str(book).zfill(3)+"/page"+str(page)+"/thumbnail.jpg"
            except:
                src = "http://design-ec.com/d/e_others_50/l_e_others_500.png"
                width = "600"
                height = "600"
                thumb = "http://design-ec.com/d/e_others_50/l_e_others_500.png"

            obj = {
                "original": src,
                "thumbnail": thumb,
                "book": str(book).zfill(3),
                "page": page,
                "width": width,
                "height": height
            }

            if text != "":
                obj["text"] = text.text.strip()

            with open(path, 'w') as outfile:
                json.dump(obj, outfile, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

        
        page += 1

       
