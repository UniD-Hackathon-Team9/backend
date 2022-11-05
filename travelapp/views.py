from django.shortcuts import render
from .constants import CLIENT_ID, CLIENT_SECRET
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from .models import Region, Place
from userapp.models import User
from .serializers import RegionSerializer, PlaceSerializer
import urllib.request
import random
import json
import ssl
from django.http import JsonResponse

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Create your views here.

def get_place_info(place):
    max_display = 5   # 20개까지만 받아오기

    url = "https://openapi.naver.com/v1/search/local?query=" + place + "&display=" + str(int(max_display))  # JSON 결과 저장
    
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", CLIENT_ID)
    req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    response = urllib.request.urlopen(req)

    rescode = response.getcode()


    if rescode==200:
        response_body = response.read()
        # print(response_body)
        result = json.loads(response_body.decode('UTF-8'))
        print("result = " + str(result['items']))
        dict_place = result['items']
        place_list = {}
        place = {}
        for i in range(len(dict_place)):
            place['title'] = dict_place[i]['title']
            place['address'] = dict_place[i]['address']
            place['description'] = dict_place[i]['category']
            place_list.update(place)

            print('dd;' + list((dict_place[i]['address']).split(" "))[1], list((dict_place[i]['address']).split(" "))[2])
            try:
                region_id = Region.objects.get(region_large=list((dict_place[i]['address']).split(" "))[1], region_small=list((dict_place[i]['address']).split(" "))[2])
                print(region_id)
            except:
                region_id = 0

            Place.objects.create(
                name=place['title'],
                description = place['description'],
                latitude = dict_place[i]['mapx'],
                longtitude = dict_place[i]['mapy'],
                region = region_id
            )

            place = {}

    
    else:
        print("Error Code:" + rescode)

    return place_list

@api_view(['GET'])
def recommend_place(request, type=None):
    # encode_type = 'json'
    # sort = 'sin'   # 관련도순

    ##### 로그인 유저 ######
    try:
        user = request.user
        loginUser = User.objects.get(pk=user.id)
        personal_type = loginUser.personal_type
        preference = loginUser.preference
    except:
        ##### 비로그인 유저 ######
        personal_type = request.GET.get('personalType')
        preference = request.GET.get('preference')


    ########### 추천 알고리즘 #################

    search_region = request.GET.get('name')
    mypositions = [
        [1,2],
        [2,3],
        [3,4],
        [1,4]
    ]
    positions = mypositions[random.randrange(0, 4)] if personal_type == "b" else [random.randrange(2, 5)]
    

    # search_food = search_region + (" 음식점")
    # search_food = urllib.parse.quote(search_food)
    # search_cafe =  search_region + (" 카페")
    # search_cafe = urllib.parse.quote(search_cafe)
    # search_spot = search_region + (" 명소")
    # search_spot = urllib.parse.quote(search_spot)
    
    place = Place.objects.raw(f'SELECT * FROM travelapp_place;')[0]

    
    # print("response = " + str(response))
    response_dict = {}
    # response_dict.update(get_place_info(search_food))
    # response_dict.update(get_place_info(search_cafe))
    # response_dict.update(get_place_info(search_spot))

    print(place)

    # serializer = RegionSerializer(json.dumps(response_dict), many=True)
    # return Response(serializer.data)
    return JsonResponse({'foo': 'bar'})



#################################################################################################3

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

            print('dd;' + list((dict_food[i]['address']).split(" "))[1], list((dict_food[i]['address']).split(" "))[2])
            region_id = Region.objects.get(region_large=list((dict_food[i]['address']).split(" "))[1], region_small=list((dict_food[i]['address']).split(" "))[2])
            print(region_id)
            Place.objects.create(
                name=dict_food[i]['title'],
                description = dict_food[i]['description'],
                latitude = dict_food[i]['mapx'],
                longtitude = dict_food[i]['mapy'],
                region = region_id
            )
    
    else:
        print("Error Code:" + rescode)
