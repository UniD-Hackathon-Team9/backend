from django.urls import path
from django.urls import re_path as url
from rest_framework.urlpatterns import format_suffix_patterns
from travelapp import views
from . import views

urlpatterns = [
    url(r'^$', views.get_place_food),
    url(r'^(?P<pk>[0-9]+)/$', views.region_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
