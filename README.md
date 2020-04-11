# aidon-elastic

*This code is based on https://github.com/skagmo/meter_reading*

What we´re trying to do here is get a reading of power compumption from HAN port, and then index the readings in Elasticsearch. This data
will then be available for graphing and analysis in Kibana.

## Installation steps include

- Prepare hardware for reading HAN port
- Install Git, docker and docker-compose on your server
- Clone this repo on your server
- Prepare OS for Elasticsearch
- Change access rights on /dev/ttyUSB0
- Launch Docker containers for elasticsearch and Kibana
- Add index templates and settings to Elasticsearch
- Build and launch Docker container for aidon-reader

## Elasticsearch node

See guidelines and tips here: https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

In particular I needed to set up vm.max_map_count kernel setting to 262144 for my Centos 7 server.
`sudo sysctl -w vm.max_map_count=262144`

## Change access right on the serial port device

`sudo chmod 0666 /dev/ttyUSB0` 


## Test that you are able to read HAN port

`python ./aidon_test.py /dev/ttyUSB0`


## Start Aidon docker containers

`docker-compose up -d`


## Check data in Kibana

Go to Kibana URL: http://localhost:5601
Alternatively try and list data directly from Elasticsearch using `curl "http://localhost:9200/aidon*/_search?pretty=true"`


### Output logs from all containers to the screen continuously

`docker-compose logs -f`


### Stop/kill and remove containers

```
docker-compose stop
docker-compose kill
docker-compose rm
```


### Delete storage volume

This command is handy to give Elasticsearch a fresh start and not remember any data or customisation from earlier.
`docker volume rm aidon-elastic_data1`

## Automatically timestamp readings as they are indexed by Elasticsearch

### Create pipeline for timestamping

```
PUT _ingest/pipeline/timestamp
{
  "description": "Adds a timestamp called timestamp to documents",
  "processors": [
    {
      "set": {
        "field": "_source.timestamp",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```

### Add timestamp pipeline, other settings, and mappings to the index template
```
PUT _template/aidon_template
{
  "index_patterns": [
    "aidon*"
  ],
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "index.default_pipeline": "timestamp"
  },
  "mappings": {
    "_source": {
      "enabled": true
    },
    "properties": {
      "il1": {
        "type": "float"
      },
      "il2": {
        "type": "float"
      },
      "meter_id": {
        "type": "keyword"
      },
      "meter_type": {
        "type": "keyword"
      },
      "p_act_in": {
        "type": "long"
      },
      "p_act_out": {
        "type": "long"
      },
      "p_react_in": {
        "type": "long"
      },
      "p_react_out": {
        "type": "long"
      },
      "timestamp": {
        "type": "date"
      },
      "ul1": {
        "type": "float"
      },
      "ul2": {
        "type": "float"
      },
      "ul3": {
        "type": "float"
      }
    }
  }
}

```


