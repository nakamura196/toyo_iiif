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

dir_id = "k5"

for file in files:

    # jsonファイルを読み込む
    f = open(file)
    # jsonデータを読み込んだファイルオブジェクトからPythonデータを作成
    data = json.load(f)
    # ファイルを閉じる
    f.close()

    id = data["id"]
    manifest = "https://nakamura196.github.io/toyo_iiif/iiif/"+dir_id+"/"+id+"/manifest.json"
    related = "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest

    rows.append([id, data["title"], "", "http://www.toyo-bunko.or.jp/library3/usingthefacilities.html", manifest, related, "", "", "東洋文庫"])

import csv

f = open('data/items.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()

            
