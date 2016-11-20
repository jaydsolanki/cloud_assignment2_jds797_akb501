from elasticsearch import Elasticsearch


def search_tweets(keyword, index_name, host=None):
    if not host:
        es = Elasticsearch()
    else:
        es = Elasticsearch(host)
    hits = es.search(index=index_name,body={"from":0, "size":5000 ,"query":{"match":{"tweet":keyword}}})
    result = []
    if hits and hits.get('hits',None) and len(hits['hits']['hits'])>0:
        for record in hits['hits']['hits']:
            tweet = record['_source']['tweet']
            lat = record['_source']['location']['lat']
            lon = record['_source']['location']['lon']
            result.append([tweet, lat, lon])
    return result


def search_tweets_geo(keyword, distance, lat, lng, index_name, host=None):
    if not host:
        es = Elasticsearch()
    else:
        es = Elasticsearch(host)
    hits = es.search(index=index_name,body={"from":0, "size":5000 ,"query":{"match":{"tweet":keyword}}, "filter":{"geo_distance":{"distance":str(distance)+"km","location":{"lat":lat, "lon":lng}}}})
    result = []
    if hits and hits.get('hits',None) and len(hits['hits']['hits'])>0:
        for record in hits['hits']['hits']:
            tweet = record['_source']['tweet']
            lat = record['_source']['location']['lat']
            lon = record['_source']['location']['lon']
            result.append([tweet, lat, lon])
    return result


def add_object_to_index(index_name, id, tweet, lat, lon, sentiment, host=None):
    if not host:
        es = Elasticsearch()
    else:
        es = Elasticsearch(host)
    es.index(index=index_name, id=id, doc_type="tweet", body={"tweet": tweet, "location": {"lat": lat, "lon": lon}, "sentiment":sentiment})

