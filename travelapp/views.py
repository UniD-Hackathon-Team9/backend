from django.shortcuts import render
from .constants import CLIENT_ID, CLIENT_SECRET
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import Region, Place
from .serializers import RegionSerializer, PlaceSerializer
import urllib.request
import json

# Create your views here.

class DataListAPI(viewsets.ModelViewSet):
    def get(self, request):
        queryset = Region.objects.all()
        print(queryset)
        serializer = RegionSerializer(queryset, many=True)
        return Response(serializer.data)


# 지역 검색 (네이버 API)
class RegionAPI(viewsets.ModelViewSet):
    search_region = urllib.parse.quote('한라산')
    # encode_type = 'json'
    # sort = 'sin'   # 관련도 순

    # max_display = 100
    # start = 1   # 출력 위치

    url = "https://openapi.naver.com/v1/search/local?query=" + search_region  # JSON 결과 저장
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    response = urllib.request.urlopen(req)

    rescode = response.getcode()
    
    if rescode==200:
        response_body = response.read()
        result = json.loads(response_body.decode('UTF-8'))
        address = result.get('items')[0]['address']
        large_region = list(address.split(' '))[0]
        small_region = list(address.split(' '))[1]
    else:
        print("Error Code:" + rescode)

    '''
    url = f"https://openapi.naver.com/v1/search/local?query={search_region}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
    headers = {
        "X-Naver-Client-Id": CLIENT_ID,
        "X-Naver-Client-Secret": CLIENT_SECRET
    }

    # HTTP 요청
    r = requests.get(url, headers=headers)
    rescode = r.getcode()
    print(rescode)

    if "200" in str(r):
        for data in enumerate(r.json()['address']):
            print(data)
    '''
    query_set = {
        'large_region': large_region,
        'small_region': small_region
    }
    serializer_class = RegionSerializer

'''
@api_view(['GET', 'POST'])
def region_list(request, format=None):
    if request.method == 'GET':

        search_region = urllib.parse.quote('한라산')


        url = "https://openapi.naver.com/v1/search/local?query=" + search_region  # JSON 결과 저장
        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", CLIENT_ID)
        req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
        response = urllib.request.urlopen(req)

        rescode = response.getcode()
        
        if rescode==200:
            response_body = response.read()
            result = json.loads(response_body.decode('UTF-8'))
            address = result.get('items')[0]['address']
            large_region = list(address.split(' '))[0]
            small_region = list(address.split(' '))[1]
        else:
            print("Error Code:" + rescode)

        if small_region == Region.GET.get('region_small') and large_region == Region.GET.get('region_large'):
            place = Place.objects.all()
        
        query_set = {
            'large_region': large_region,
            'small_region': small_region
        }
        serializer = RegionSerializer(query_set, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RegionSerializer(data=request.data)
        if serializer.is_vaid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        '''

@api_view(['GET', 'PUT', 'DELETE'])
def region_detail(request, pk, format=None):
    try:
        region = Region.objects.get(pk=pk)
    except Region.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RegionSerializer(region)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RegionSerializer(region, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        region.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def region_set(request, format=None):
    if request.method == 'GET':
        print("request: " + str(request))
        print(request.GET.get('name'))
        place = Place.objects.get(name=str(request.name))
        print(request.name)
        search_region = urllib.parse.quote(place.name)


        url = "https://openapi.naver.com/v1/search/local?query=" + search_region  # JSON 결과 저장
        req = urllib.request.Request(url)
        req.add_header("X-Naver-Client-Id", CLIENT_ID)
        req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
        response = urllib.request.urlopen(req)
        print(response)

        rescode = response.getcode()
        
        if rescode==200:
            response_body = response.read()
            result = json.loads(response_body.decode('UTF-8'))
            address = result.get('items')[0]['address']
            large_region = list(address.split(' '))[0]
            small_region = list(address.split(' '))[1]
        else:
            print("Error Code:" + rescode)

        if small_region == Region.GET.get('region_small') and large_region == Region.GET.get('region_large'):
            region = Region.objects.filter(region_small=small_region, region_large=large_region)
            place.region = region.id
            place.save()
        
        query_set = {
            'large_region': large_region,
            'small_region': small_region
        }
        serializer = RegionSerializer(query_set, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = RegionSerializer(data=request.data)
        if serializer.is_vaid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_place_food(request, type=None):
    max_display = 20   # 20개까지만 받아오기
    encode_type = 'json'
    sort = 'sin'   # 관련도순

    search_region = request.GET.get('name')
    search_region += (" 음식점")
    search_region = urllib.parse.quote(search_region)
    url = "https://openapi.naver.com/v1/search/local?query=" + search_region + "&display=" + str(int(max_display))  # JSON 결과 저장
    
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    response = urllib.request.urlopen(req)
    # print("response = " + str(response))

    rescode = response.getcode()

    if rescode==200:
        response_body = response.read()
        # print(response_body)
        result = json.loads(response_body.decode('UTF-8'))
        print("result = " + str(result['items']))
        dict_food = result['items']
        food_list = {}
        food = {}
        for i in range(len(dict_food)):
            food['title'] = dict_food[i]['title']
            food['address'] = dict_food[i]['address']
            food_list.update(food)
            food = {}
            
            print(dict_food[i]['address'][1], dict_food[i]['address'][2])
            region_id = Region.objects.filter(region_large=dict_food[i]['address'][1], region_small=dict_food[i]['address'][2])

            Place.objects.create(
                name=dict_food[i]['title'],
                description = dict_food[i]['description'],
                latitude = dict_food[i]['mapx'],
                longtitude = dict_food[i]['mapy'],
                address = region_id
            )
    
    else:
        print("Error Code:" + rescode)
