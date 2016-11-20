import csv
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import boto3


# Variables that contains the user credentials to access Twitter API
consumer_key='knSmWG4Quxx1J6d6fBjq8o6sC'
consumer_secret='pGAfUp6fPL68x6RwsMrvSh68UkRJ0RXVpQDgqTgJAA8M2f0j8v'
access_token='95882254-XdfWIqxNfuleqNG968qGGAn4bssQW5aiuDhKUab2r'
access_token_secret='zyPnWsNusGYZAFKKxTI6JzLVrjhkVn5xQGvnZbZRTsWKx'

sqs = boto3.resource("sqs")
queue = sqs.create_queue(QueueName='test', Attributes={"DelaySeconds":"5"})


# This is a listener that appends the tweet text, longitude and latitude to a csv file.
class StdOutListener(StreamListener):

    def on_data(self, data):
        global queue
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
                data =  {
                            'Id': {'DataType': 'Number', 'StringValue': str(id)},
                            'Tweet': {'DataType': 'String', 'StringValue': str(tweet)},
                            'Latitude': {'DataType': 'Number', 'StringValue': str(lat)},
                            'Longitude': {'DataType': 'Number', 'StringValue': str(lon)}
                        }
                print (data)
                queue.send_message(MessageBody="TweetInfo", MessageAttributes=data)
        except Exception as e:
            print ("Error: "+str(e))

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(languages=['en'], track=['starbucks','android','national geographic','pets','music'])
