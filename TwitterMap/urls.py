from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^search/', views.search, name="search"),
    url(r'^search_query/', views.search_query, name="search_query"),
    url(r'^geo_query/', views.geo_query, name="geo_query")
]
