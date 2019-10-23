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
rows.append(["ID", "title", "Thumbnail", "rights", "manifest", "Relation", "viewingDirection", "viewingHint", "attribution"])
rows.append(["http://purl.org/dc/terms/identifier", "http://purl.org/dc/terms/title", "http://xmlns.com/foaf/0.1/thumbnail", "http://purl.org/dc/terms/rights", "http://schema.org/url", "http://purl.org/dc/terms/relation", "http://iiif.io/api/presentation/2#viewingDirection", "http://iiif.io/api/presentation/2#viewingHint"])
rows.append(["Literal", "Literal", "Resource", "Resource", "Resource"])
rows.append([])

for file in files:

    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()

    rows.append([data["id"], data["title"]])

import csv

f = open('data/items.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

            
