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

    # if "kansai" not in colections_uri:
    #    continue

    attr = c["label"]

    print(attr)

    data = requests.get(colections_uri, headers={"content-type": "application/json"}).json()

    manifests = data["manifests"]

    for i in range(len(manifests)):
        manifest = manifests[i]

        manifest_uri = manifest["@id"]
        

        id = hashlib.md5(manifest_uri.encode('utf-8')).hexdigest()

        file_path = "data/"+dir+"/json/"+id+".json"
        print(manifest_uri)

        if not os.path.exists(file_path):

            try:
                res = urllib.request.urlopen(manifest_uri)
                # json_loads() でPythonオブジェクトに変換
                data = json.loads(res.read().decode('utf-8'))

                fw = open(file_path, 'w')
                json.dump(data, fw, ensure_ascii=False)
            except Exception as err:
                print("E1\t"+str(err))

                if "utf-8-sig" in str(err):
                    try:
                        data = json.loads(res.read().decode('utf-8-sig'))

                        print(data)

                        fw = open(file_path, 'w')
                        json.dump(data, fw, ensure_ascii=False)
                    except Exception as err2:
                        print("E2\t"+str(err2))

                        if "Expecting value" in str(err2):

                            try:

                                headers = {"content-type": "application/json"}
                                r = requests.get(manifest_uri, headers=headers)
                                data = r.json()

                                fw = open(file_path, 'w')
                                json.dump(data, fw, ensure_ascii=False)
                            except Exception as e3:
                                print("E3\t"+str(e3))

                else:

                    '''
                    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
                    req = urllib.request.Request(url=manifest_uri)
                    #context=TLSv1に指定
                    res = urllib.request.urlopen(req,context=context)
                    data = json.loads(res.read().decode('utf-8'))

                    print(data)

                    fw = open(file_path, 'w')
                    json.dump(data, fw, ensure_ascii=False)
                    '''
                    
                    print("aaa")

