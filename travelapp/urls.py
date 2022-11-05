from django.urls import path, include
from django.urls import re_path as url
# from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from travelapp import views
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('regions', RegionAPI)


urlpatterns = [
    # path('', include(router.urls)),
    # path('api/regions', DataListAPI.as_view()),
    # path('get_region/<int:pk>', RegionAPI.as_view()),
    url(r'^$', views.recommend_place),
    url(r'^(?P<pk>[0-9]+)/$', views.region_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
