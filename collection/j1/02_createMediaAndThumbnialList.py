import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob
import requests

files = glob.glob("tmp/*.json")

rows = []
rows.append(["ID", "Original", "Thubmnail", "Width", "Height"])

rows2 = []
rows2.append(["ID", "Thumbnail"])

for file in sorted(files):

    filename = file.split("/")[-1]
    print(filename)

    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()

    arr = data["arr"]

    for i in range(len(arr)):

        image = arr[i]

        print(image)

        original = image.replace("http://124.33.215.236", "https://toyo-iiif.s3.us-east-2.amazonaws.com").replace(".jpg", "/info.json")

        try:

            print(original)
            r = requests.get(original)
            info = r.json()

            size = info["sizes"][0]

            thumbnail = original.replace("info.json", "full/"+str(size["width"])+",/0/default.jpg")

            if i == 0:
                rows2.append([data["id"], thumbnail])

            rows.append([data["id"], original, thumbnail, info["width"], info["height"]])
        except:
            print("Error.")

import csv

f = open('data/media.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

f = open('data/thumbnail.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows2)

f.close()




       
