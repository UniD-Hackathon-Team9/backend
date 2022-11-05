from django.test import TestCase
import urllib.request
import requests
import pandas as pd
import json

CLIENT_ID='rcpSRqFxxhEfRkZjhZiy'
CLIENT_SECRET='0eERkQtJuE'

# Create your tests here.
search_region = urllib.parse.quote('성산 음식점')
encode_type = 'json'
sort = 'sin'   # 관련도 순

max_display = 30   # 출력 수
start = 1   # 출력 위치
# headers = {
#     "X-Naver-Client-Id": CLIENT_ID,
#     "X-Naver-Client-Secret": CLIENT_SECRET
# }


url = "https://openapi.naver.com/v1/search/local?query=" + search_region + "&display=" + str(int(max_display))  # JSON 결과 저장
# url = f"https://openapi.naver.com/v1/search/local.{encode_type}?query={search_region}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"
# r = requests.get(url, headers=headers)

# if r.status_code == 200:
#     if len(res) == 0:
#         res = pd.DataFrame({
#             'name': [None],
#             'description': [None],
#             'mapx': [None],
#             'mapy': [None]
#         })
#     else:
#         res = pd.DataFrame(r.json()['items'])
# else:
#     print("error with errorCode: " + r.status_code)


req = urllib.request.Request(url)
req.add_header("X-Naver-Client-Id", CLIENT_ID)
req.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
response = urllib.request.urlopen(req)
print(response)
rescode = response.getcode()

if rescode==200:
    response_body = response.read()
    result = json.loads(response_body.decode('UTF-8'))
    print(result)
    address = result.get('items')[0]['address']
    large_region = list(address.split(' '))[1]
    small_region = list(address.split(' '))[2]
    print(address)
    print(large_region)
    print(small_region)
else:
    print("Error Code:" + rescode)

