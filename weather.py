"""
Authors: Armando, Lily, Eduardo, Gabe
Course: CST-205
Date: 05/14/2024
Summary: Runs a flask app that allows for the user to enter in a city name
and brings a second page with some weather information of that city currently.
=======
Gabe and Armando mostly worked on this python file 
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

my_key = "77b4df041ddc47e427d8799ea237cb80" # API key

app = Flask(__name__)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST']) # route to homepage
def homepage():
    global city_name
    city_name = request.form.get('citytxtbox')
    return render_template('home.html', city_name = city_name)


@app.route('/details')
def link(): # route to details page
    city_name = request.args.get('citytxtbox')

    limit = 1

    geo_endpoint = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={my_key}"
    # geo test endpoint:
    # https://api.openweathermap.org/geo/1.0/direct?q=Monterey&limit=1&appid=77b4df041ddc47e427d8799ea237cb80

    # retrieves longitude and latitude from GeoEncoder API
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
    # retrieves the weather data to be displayed on details page
    try:
        wreq = requests.get(weather_endpoint)
        weatherdata = wreq.json()
    except:
        print("Weather Endpoint Fail Error!")


    
    icon_code = weatherdata["weather"][0]["icon"]

    # map_endpoint = f"https://tile.openweathermap.org/map/{op}/{zoom}/{x}/{y}.png?appid={my_key}"
    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png" #endpoint for icon retrieval

    urllib.request.urlretrieve(icon_url, "static/images/weather_icon.png")
    
    my_src = Image.open('weather_icon.png')
    
    return render_template('Weather_Details.html', city_name = city_name, geodata = geodata, weatherdata = weatherdata, icon_name = "weather_icon.png")

