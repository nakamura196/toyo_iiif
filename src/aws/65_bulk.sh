echo data/tmp/iiif/bulk_881.json
curl -XPOST -s -# -O https://search-nakamura1962-c7fo7icjwe2j6u2qsxf3mp2lda.us-east-2.es.amazonaws.com/_bulk --data-binary @data/tmp/iiif/bulk_881.json -H 'Content-Type: application/json'