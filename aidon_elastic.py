#!/usr/bin/python


import serial, time, sys, json
from aidon_obis import *
from elasticsearch.client.ingest import IngestClient
from elasticsearch import Elasticsearch

# Define variables
es_index='aidon-2020'
es_server='elastic1'
es_port=9200

def create_pipeline():
  pipeline_body = {
    "description": "Adds timestamp called timestamp to documents",
    "processors": [
      {
        "set": {
        "field": "_source.timestamp",
        "value": "{{_ingest.timestamp}}"
        }
      }
    ]
  }
  p = IngestClient(es)
  p.put_pipeline(id='timestamp', body=pipeline_body )

def create_index():
  index_settings = {
    "settings" : {
      "index" : {
        "number_of_shards" : "1",
        "default_pipeline" : "timestamp",
        "number_of_replicas" : "0"
      }
    }
  }
  response = es.indices.create(
      index=es_index,
      body=index_settings,
      ignore=400 # ignore 400 already exists code
  )
  if 'acknowledged' in response:
    if response['acknowledged'] == True:
      print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
  # catch API error response
  elif 'error' in response:
    print ("ERROR:", response['error']['root_cause'])
    print ("TYPE:", response['error']['type'])
  # print out the response:
  print ('\nresponse:', response)

def aidon_callback(fields):
    res = es.index(index=es_index,doc_type='_doc',body=json.dumps(fields))

if len (sys.argv) != 2:
	print "Usage: ... <serial_port>"
	sys.exit(0)

es=Elasticsearch([{'host':es_server,'port':es_port}])
create_pipeline()
create_index()

ser = serial.Serial(sys.argv[1], 2400, timeout=0.05, parity=serial.PARITY_NONE)
a = aidon(aidon_callback)

while(1):
	while ser.inWaiting():
		a.decode(ser.read(1))
	time.sleep(0.01)
