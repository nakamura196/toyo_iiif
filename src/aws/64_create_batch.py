import json
from SPARQLWrapper import SPARQLWrapper
import urllib.parse
import requests
import csv
import os
import glob
import sys
import argparse

dir = "tmp"
files = glob.glob("data/"+dir+"/*.json")

rows = []

for file in files:

    filename = file.split("/")[-1]

    rows.append("echo "+file)
    rows.append("curl -XPOST -s -# -O https://search-nakamura1962-c7fo7icjwe2j6u2qsxf3mp2lda.us-east-2.es.amazonaws.com/_bulk --data-binary @data/"+dir+"/"+filename+" -H 'Content-Type: application/json'")


f = open("65_bulk.sh", 'w')

import csv

f.write("\n".join(rows))

f.close()

