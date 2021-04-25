import sys
from io import BytesIO

import requests
from PIL import Image

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response_1 = requests.get(geocoder_api_server, params=geocoder_params)

if not response_1:
    pass

json_response_1 = response_1.json()
toponym = json_response_1["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")


search_api_server = "https://search-maps.yandex.ru/v1/"

api_key = "d0ce2ab6-de1b-471e-abc6-91173b1eae61"

address_ll = ','.join([toponym_longitude, toponym_lattitude])

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response_2 = requests.get(search_api_server, params=search_params)
if not response_2:
    pass

json_response_2 = response_2.json()

organization = json_response_2["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
print(json_response_2)

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
print(org_address)
map_params = {
    "ll": address_ll,
    "l": "map",
    "pt": "{0},pm2dgl".format(org_point) + ',org'
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()