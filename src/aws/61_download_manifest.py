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

import ssl

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

    print(attr)

    data = requests.get(colections_uri, headers={"content-type": "application/json"}).json()

    manifests = data["manifests"]

    for i in range(len(manifests)):
        manifest = manifests[i]

        manifest_uri = manifest["@id"]
        

        id = hashlib.md5(manifest_uri.encode('utf-8')).hexdigest()

        file_path = "data/json/"+id+".json"
        print(manifest_uri)

        if not os.path.exists(file_path):

            try:
                data = requests.get(manifest_uri, headers={"content-type": "application/json"}).json()

                fw = open(file_path, 'w')
                json.dump(data, fw, ensure_ascii=False)
            except Exception as err:
                print("E1\t"+str(err))
