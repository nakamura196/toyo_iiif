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

colections_uri = "https://raw.githubusercontent.com/nakamura196/toyo_iiif/master/docs/iiif/toyo/collection/top.json"

rows = []
 
url = colections_uri
res = urllib.request.urlopen(url)
# json_loads() でPythonオブジェクトに変換
data = json.loads(res.read().decode('utf-8'))

collections = data["collections"]

for c in collections:
    colections_uri = c["@id"]

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
        if isinstance(label, list):
            for obj in label:
                if obj["@language"] == "ja":
                    tmp = obj["@value"]
            label = tmp

        id = hashlib.md5(manifest_uri.encode('utf-8')).hexdigest()

        file_path = "data/json/"+id+".json"

        obj = {
            "_id": id,
            "accessInfo": attr,
            "image": "https://www.gumtree.com/static/1/resources/assets/rwd/images/orphans/a37b37d99e7cef805f354d47.noimage_thumbnail.png",
            "label": label,
            "sourceInfo": "東洋文庫IIIFコレクション",
            "url": "http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest="+manifest_uri,
            "media": "IIIF",
            "manifest": manifest_uri
        }

        if os.path.exists(file_path):
            try:
                with open(file_path) as f:
                    df = json.load(f)

                    if "thumbnail" in df:
                        thumbnail = df["thumbnail"]["@id"]
                        obj["image"] = thumbnail

                    description = []

                    if "metadata" in df:

                        metadata = df["metadata"]

                        for m in metadata:
                            description.append(m["label"]+" : "+str(m["value"]))
                        obj["description"] = description
            except Exception as e:
                print("error\t"+manifest_uri+"\t"+str(e))

        rows.append(obj)

fw = open("data/list.json", 'w')
json.dump(rows, fw, ensure_ascii=False)
