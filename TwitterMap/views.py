from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from .elastic_search import search_tweets, search_tweets_geo
from django.conf import settings


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
