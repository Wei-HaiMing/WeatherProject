"""
Authors: Armando, Lily, Eduardo, Gabe
"""
import json
from pprint import pprint
import urllib.request
import requests

my_key = "77b4df041ddc47e427d8799ea237cb80"

# payload = {
#     "q": "Salinas",
#     "appid": my_key,
#     "limit": 1
# }
city_name = "Salinas"
limit = 1

geo_endpoint = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={my_key}"

try:
    r = requests.get(geo_endpoint)
    data = r.json()
    pprint(data)
except:
    print("geo fail, please try again")

weather_endpoint = f"https://api.openweathermap.org/data/2.5/weather?lat={data[0]["lat"]}&lon={data[0]["lon"]}&appid={my_key}"

try:
    r = requests.get(weather_endpoint)
    data = r.json()
    pprint(data)
except:
    print("weather fail, please try again")