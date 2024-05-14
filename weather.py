"""
Authors: Armando, Lily, Eduardo, Gabe
"""
from flask import  Flask, render_template, request, redirect
from PIL import Image
from flask_bootstrap import Bootstrap5
import random
import json
from pprint import pprint
import urllib.request
import requests
import numpy as np

my_key = "77b4df041ddc47e427d8799ea237cb80"

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def homepage():
    global city_name
    city_name = request.form.get('citytxtbox')
    return render_template('home.html', city_name = city_name)


@app.route('/details')
def link():
    city_name = request.args.get('citytxtbox')

    limit = 1

    geo_endpoint = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={my_key}"
    # geo test endpoint:
    # https://api.openweathermap.org/geo/1.0/direct?q=Monterey&limit=1&appid=77b4df041ddc47e427d8799ea237cb80

    try:
        greq = requests.get(geo_endpoint)
        geodata = greq.json()
    except:
        print("Geo Endpoint Fail Error!")
    
    lat = geodata[0]['lat']
    lon = geodata[0]['lon']


    weather_endpoint = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={my_key}"
    # weather test endpoint
    # https://api.openweathermap.org/data/2.5/weather?lat=36.600256&lon=-121.8946388&appid=77b4df041ddc47e427d8799ea237cb80

    try:
        wreq = requests.get(weather_endpoint)
        weatherdata = wreq.json()
    except:
        print("Weather Endpoint Fail Error!")

    op = "clouds_new"
    zoom = 2
    x = 2
    y = 2
    icon_code = weatherdata["weather"][0]["icon"]

    map_endpoint = f"https://tile.openweathermap.org/map/{op}/{zoom}/{x}/{y}.png?appid={my_key}"
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

    urllib.request.urlretrieve(icon_url, "static/images/weather_icon.png")
    
    my_src = Image.open('weather_icon.png')
    # my_src.show()

    # try:
    #     map_req = requests.get(map_endpoint)    
    #     # print(f"request thing {map_data}")

    #     # map_img = Image.open(map_img)
    #     # mapdata = map_req.json()
    #     # map_img.show()
    # except:
    #     print("Map Endpoint Fail Error!")

    pprint(f"geodata->{geodata}")
    pprint(f"weatherdata->{weatherdata}")
    # pprint(mapdata.type())
    return render_template('Weather_Details.html', city_name = city_name, geodata = geodata, weatherdata = weatherdata, icon_name = "weather_icon.png")