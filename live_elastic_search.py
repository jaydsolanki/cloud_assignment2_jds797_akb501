from elasticsearch import Elasticsearch
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import sys

# Variables that contains the user credentials to access Twitter API
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''


# This is a listener that appends the tweet text, longitude and latitude to a csv file.
class StdOutListener(StreamListener):
    def on_data(self, data):
        if len(host)==0:
            es = Elasticsearch()
        else:
            es = Elasticsearch(host)
        try:
            json_data = json.loads(data)
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
                print (lat)
                es.index(index=index_name, id=id, doc_type="tweet", body={"tweet": tweet, "location": {"lat": lat, "lon": lon}})
        except Exception as e:
            print("ERROR: " + str(e))

    def on_error(self, status):
        print(status)

if len(sys.argv)<3:
    print ("Usage\n\npython live_elastic_search.py <index_name> <host of elastic search>\n")
if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    index_name = sys.argv[1]
    host = [sys.argv[2] if sys.argv[2]!="" else []
    stream.filter(track=['starbucks','android','national geographic','pets','music'])
