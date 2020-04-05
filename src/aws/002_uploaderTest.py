import sys
from classes import uploader
import csv
import glob
import json
import requests
import hashlib
import os

INDEX = "toyo_items"
HOST = 'search-nakamura196-rgvfh3jsqpal3gntof6o7f3ch4.us-east-1.es.amazonaws.com'
REGION = 'us-east-1'
PROFILE_NAME = 'default'

files = glob.glob("data/json/*.json")
files = sorted(files)

all_bodies = []

colections_uri = "https://raw.githubusercontent.com/nakamura196/toyo_iiif/master/docs/iiif/toyo/collection/top.json"

rows = []
 
url = colections_uri
res = requests.get(url)
# json_loads() でPythonオブジェクトに変換
data = res.json()

collections = data["collections"]

for c in collections:
    colections_uri = c["@id"]

    attr = c["label"]
    if len(attr.split(" (")) == 2:
        attr = attr.split(" (")[0]

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

        # ------

        body = {
            "_type" : "_doc",
            "_index" : INDEX,
            "_id": id,
            "_image": ["https://www.gumtree.com/static/1/resources/assets/rwd/images/orphans/a37b37d99e7cef805f354d47.noimage_thumbnail.png"],
            "_title": [label],
            "_url": ["http://da.dl.itc.u-tokyo.ac.jp/mirador/?manifest="+manifest_uri],
            "_media": ["IIIF"],
            "_manifest": [manifest_uri],

            "データベース": ["東洋文庫IIIFコレクション"],
        }

        if os.path.exists(file_path):
            try:
                with open(file_path) as f:
                    df = json.load(f)

                    if "thumbnail" in df:
                        thumbnail = df["thumbnail"]["@id"]
                        body["_image"] = [thumbnail]

                    description = []

                    if "metadata" in df:

                        metadata = df["metadata"]

                        for m in metadata:
                            label = m["label"]
                            value = str(m["value"])
                            if label not in body:
                                body[label] = []
                            body[label].append(value)
            except Exception as e:
                print("error\t"+manifest_uri+"\t"+str(e))

        all_bodies.append(body)

uploader.Uploader.main(
    index=INDEX, 
    host=HOST, 
    region=REGION, 
    profile_name=PROFILE_NAME, 
    all_body=all_bodies)
