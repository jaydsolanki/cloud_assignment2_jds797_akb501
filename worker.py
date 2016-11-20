import boto3
import multiprocessing
import time
import random
# from alchemyapi import AlchemyAPI
import boto3
import json

sqs = boto3.resource('sqs')
sns = boto3.client('sns')
queue = sqs.get_queue_by_name(QueueName='test')
# alchemiapi = AlchemyAPI()
# sudo pip3 install --upgrade watson-developer-cloud
sentiment = ["positive","negative","neutral"]
arn = ''
def worker_main(queue):
    while True:
        messages = queue.receive_messages(MessageAttributeNames=['Id', 'Tweet', 'Latitude', 'Longitude'])
        if len(messages)>0:
            for message in messages:
                # Get the custom author message attribute if it was set
                if message.message_attributes is not None:
                    id = message.message_attributes.get('Id').get('StringValue')
                    tweet = message.message_attributes.get('Tweet').get('StringValue')
                    lat = message.message_attributes.get('Latitude').get('StringValue')
                    lng = message.message_attributes.get('Longitude').get('StringValue')
                    senti = sentiment[random.randint(0,2)]
                    # try:
                    #     respone = alchemiapi.sentiment('text',tweet)
                    #     senti = response.get('docSentiment').get('type')
                    # except:
                    #     senti = "neutral"
                    # Using SNS
                    sns_message = {"id":id, "tweet":tweet, "lat":lat, "lng": lng, "sentiment":senti}
                    sns.publish(TargetArn=arn, Message=json.dumps({'default':json.dumps(sns_message)}))
                # Print out the body and author (if set)
                # print('Id: {0}; Tweet: {1}; Latitude: {2}; Longitude: {3}; sentiment: {4}'.format(id,tweet,lat,lng,senti))
                # Let the queue know that the message is processed
                message.delete()
        else:
            time.sleep(1)

pool = multiprocessing.Pool(10, worker_main, (queue,))


'''
{
  "url": "https://gateway-a.watsonplatform.net/calls",
  "note": "It may take up to 5 minutes for this key to become active",
  "apikey": "354656d61227e678ad152a63dbd5b93cdeea4b93"
}
'''