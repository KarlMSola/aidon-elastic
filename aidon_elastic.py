#!/usr/bin/pythonr

import serial, time, sys, json
from aidon_obis import *
from elasticsearch import Elasticsearch

PUT _ingest/pipeline/timestamp
{
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

settings = {
  "settings" : {
    "index" : {
      "number_of_shards" : "1",
      "default_pipeline" : "timestamp",
      "number_of_replicas" : "0"
    }
  }
}

response = elastic_client.indices.create(
    index="some_new_index",
    body=mapping,
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



if len (sys.argv) != 2:
	print "Usage: ... <serial_port>"
	sys.exit(0)

es=Elasticsearch([{'host':'elastic1','port':9200}])

def aidon_callback(fields):
    res = es.index(index='aidon-2020',doc_type='_doc',body=json.dumps(fields))

ser = serial.Serial(sys.argv[1], 2400, timeout=0.05, parity=serial.PARITY_NONE)
a = aidon(aidon_callback)

while(1):
	while ser.inWaiting():
		a.decode(ser.read(1))
	time.sleep(0.01)

