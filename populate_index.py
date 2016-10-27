from elasticsearch import Elasticsearch
import json


def populate_index(file_name, index_name, host=None):
    if not host:
        es = Elasticsearch()
    else:
        es = Elasticsearch(host)
    f = open(file_name, 'r')
    mapping = {"mappings": {
        "tweet": {
            "properties": {
                "tweet": {
                    "type": "string"
                },
                "location": {
                    "type": "geo_point"
                }
            }
        }
    }
    }
    es.indices.create(index=index_name, body=mapping, ignore=400)
    for line in f:
        if line.strip() == "":
            continue
        try:
            json_data = json.loads(line)
            tweet = json_data['text']
            id = str(json_data['id'])
            lon = None
            lat = None
            if json_data['coordinates']:
                lon = float(json_data['coordinates']['coordinates'][0])
                lat = float(json_data['coordinates']['coordinates'][1])
            elif 'place' in json_data.keys() and json_data['place']:
                lon = float(json_data['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['place']['bounding_box']['coordinates'][0][0][1])
            elif 'retweeted_status' in json_data.keys() and 'place' in json_data['retweeted_status'].keys() and json_data['retweeted_status']['place']:
                lon = float(json_data['retweeted_status']['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['retweeted_status']['place']['bounding_box']['coordinates'][0][0][1])
            elif 'quoted_status' in json_data.keys() and 'place' in json_data['quoted_status'].keys() and json_data['quoted_status']['place']:
                lon = float(json_data['quoted_status']['place']['bounding_box']['coordinates'][0][0][0])
                lat = float(json_data['quoted_status']['place']['bounding_box']['coordinates'][0][0][1])
            if lat and lon:
                es.index(index=index_name, id=id, doc_type="tweet", body={"tweet": tweet, "location": {"lat": lat, "lon": lon}})
        except Exception as e:
            print("ERROR: " + str(e))
    f.close()


populate_index("tweet_location.txt", "tweet-index", ["https://search-jds797-gr2rzisoplktc2g7orat65jfci.us-west-2.es.amazonaws.com"])
