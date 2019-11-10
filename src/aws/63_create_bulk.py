import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import csv
import os
import glob
import sys
import argparse
import csv
import shutil

rows = []
odir = "data/tmp"

shutil.rmtree(odir)
os.mkdir(odir)


count = 0

def output(rows):
    f = open(odir+"/bulk_"+str(count)+".json", 'w')

    rows.append("")

    f.write("\n".join(rows))

    f.close()

    rows = []

    return rows

files = glob.glob("data/list.json")

a = 5000

for file in files:

    with open(file) as f:
        df = json.load(f)
        
        for obj in df:
            id = obj["_id"].split("/")[-1].split("#")[0]
            rows.append(json.dumps({ "index" : { "_index": "toyo", "_type" : "_doc", "_id" : id } }))
            
            obj.pop('_id')
            
            rows.append(json.dumps(obj))

            count += 1

            if count % a == 0:
                rows = output(rows)

rows = output(rows)

