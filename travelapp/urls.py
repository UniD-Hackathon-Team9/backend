from django.urls import path
from django.urls import re_path as url
from rest_framework.urlpatterns import format_suffix_patterns
from travelapp import views
from . import views

urlpatterns = [
    url(r'^$', views.recommend_place),
]

urlpatterns = format_suffix_patterns(urlpatterns)
