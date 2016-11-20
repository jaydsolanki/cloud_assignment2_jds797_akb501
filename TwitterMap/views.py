from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .elastic_search import search_tweets, search_tweets_geo, add_object_to_index
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import urllib2
from .models import NewTweets
import time
from elasticsearch import Elasticsearch


def get_credentials(credentials_file):
 f = open(credentials_file, 'r')
 data = f.read().split("\n")
 f.close()
 return data[0].split(":")[1], data[1].split(":")[1], data[2].split(":")[1], data[3].split(":")[1]


def index(request):
    context = {"title":"Home"}
    print(getattr(settings, "INDEX_NAME", None))
    print(getattr(settings, "HOST_NAME", None))
    return render(request, 'index.html', context)


def search(request):
    context = {"keywords" : ["starbucks", "android", 'national geographic','pets','music']}
    context['title'] = "Search"
    return render(request, 'search.html', context)


def search_query(request):
    if request.method=="GET":
        return redirect("/search")
    if request.method=="POST":
        selected_keyword = request.POST['selected_keyword']
        result = search_tweets(selected_keyword, getattr(settings, "INDEX_NAME", None), getattr(settings, "HOST_NAME", None))
        response = {"tweet_coordinates":result, "num_records":len(result)}
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def geo_query(request):
    if request.method=="GET":
        return redirect("/search")
    if request.method=="POST":
        selected_keyword = request.POST['selected_keyword']
        distance = float(request.POST['distance'])
        lat = float(request.POST['lat'])
        lng = float(request.POST['lng'])
        result = search_tweets_geo(selected_keyword, distance, lat, lng, getattr(settings, "INDEX_NAME", None), getattr(settings, "HOST_NAME", None))
        response = {"tweet_coordinates":result, "num_records":len(result)}
        return HttpResponse(json.dumps(response), content_type="application/json", status=200)


def poll_data(request):
    while True:
        data = NewTweets.objects.all()
        if len(data)==0:
            time.sleep(0.5)
        else:
            tweets = []
            for d in data:
                tweets.append({"id":d.id, "tweet": d.tweet, "lat": d.lat, "lng":d.lng, "sentiment": d.sentiment})
            response = {"new_tweets": tweets}
            NewTweets.objects.all().delete()
            return HttpResponse(json.dumps(response), content_type="application/json", status=200)


@csrf_exempt
def sns_handler(request):
    if request.method=="GET":
        context = {"title":"Home"}
        return render(request, "index.html", context)
    else:
        headers = json.loads(request.body)
        print("Serving SNS POST Request")
        if 'Type' in headers.keys():
            if headers['Type']=="SubscriptionConfirmation":
                print("Received Confirmation Request")
                subscribeUrl = headers['SubscribeURL']
                responseData = urllib2.urlopen(subscribeUrl).read()
                print("Subscribed to SNS")
            elif headers['Type']=="Notification":
                print ("Received a new message: "+str(headers["Message"]))
                message = json.loads(headers["Message"])
                id = message.get('id')
                tweet = message.get('tweet')
                lat = message.get("lat")
                lng = message.get("lng")
                sentiment = message.get("senti")
                index_name = getattr(settings, "INDEX_NAME", None)
                host = getattr(settings, "HOST_NAME", None)
                add_object_to_index(index_name, id, tweet, lat, lng, sentiment, host)
                new_tweet = NewTweets(id=id, tweet=tweet, lat=lat, lng=lng, sentiment=sentiment)
                new_tweet.save()
        return render(request, "data.html", {"post_params": str(request.POST)})
