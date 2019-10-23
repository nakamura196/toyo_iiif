import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import csv
import os
import glob
import sys
import argparse
import json
import urllib.request
import hashlib
import urllib.parse

colections_uri = "https://nakamura196.github.io/toyo_iiif/iiif/toyo/collection/top.json"

dir = "iiif"

rows = []
 
url = colections_uri
res = urllib.request.urlopen(url)
# json_loads() でPythonオブジェクトに変換
data = json.loads(res.read().decode('utf-8'))

collections = data["collections"]

for c in collections:
    colections_uri = c["@id"]

    if colections_uri == "https://nakamura196.github.io/iiif/data/collection/collections/ndl.json":
        continue

    attr = c["label"]
    if len(attr.split(" (")) == 2:
        attr = attr.split(" (")[0]

    print(attr)

    data = requests.get(colections_uri, headers={"content-type": "application/json"}).json()

    manifests = data["manifests"]

    for i in range(len(manifests)):
        manifest = manifests[i]

        manifest_uri = manifest["@id"]
        
        label = manifest["label"]

        id = hashlib.md5(manifest_uri.encode('utf-8')).hexdigest()

        file_path = "data/"+dir+"/json/"+id+".json"

        obj = {
            "_id": id,
            "accessInfo": attr,
            "image": "https://www.gumtree.com/static/1/resources/assets/rwd/images/orphans/a37b37d99e7cef805f354d47.noimage_thumbnail.png",
            "label": label,
            "sourceInfo": "東洋文庫IIIFコレクション",
            "url": "http://universalviewer.io/examples/uv/uv.html#?manifest="+manifest_uri,
            "media": "IIIF"
        }

        if os.path.exists(file_path):
            try:
                with open(file_path) as f:
                    df = json.load(f)
                    thumbnail = df["thumbnail"]["@id"]
                    obj["image"] = thumbnail
            except Exception as e:
                print(e)

        rows.append(obj)

fw = open("data/"+dir+"/list.json", 'w')
json.dump(rows, fw, ensure_ascii=False)
