import urllib.request
from bs4 import BeautifulSoup
from time import sleep
import json
import hashlib
import os
from PIL import Image
import glob

files = glob.glob("tmp/*.json")

rows = []
rows.append(["ID", "Page", "Text"])

for file in sorted(files):

    filename = file.split("/")[-1]
    tmp = filename.replace(".json", "").split("_")
    page = int(tmp[1])

    if page >= 2:
        
        print(filename)

        # jsonファイルを読み込む
        f = open(file)
        # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
        data = json.load(f)
        # ファイルを閉じる
        f.close()

        text = data["text"]

        if text != "":

            rows.append([tmp[0], page - 1, text])

import csv

f = open('data/text.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()




       
