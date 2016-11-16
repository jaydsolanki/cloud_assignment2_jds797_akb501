import csv
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Variables that contains the user credentials to access Twitter API
consumer_key=''
consumer_secret=''
access_token=''
access_token_secret=''



# This is a listener that appends the tweet text, longitude and latitude to a csv file.
class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(languages=['en'], track=['starbucks','android','national geographic','pets','music'])
