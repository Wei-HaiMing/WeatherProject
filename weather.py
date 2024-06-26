"""
Authors: Armando, Lily, Eduardo, Gabe
Course: CST-205
Date: 05/14/2024
Summary: Runs a flask app that allows for the user to enter in a city name
and brings a second page with some weather information of that city currently.
GitHub Link: https://github.com/Wei-HaiMing/WeatherProject
=======
Gabe and Armando mostly worked on this python file 
Armando: I worked on understanding the parameters that the API we used
and how to retrieve the correct information in order for city name 
searches to function properly. Also retrieved and displayed weather
icon on the weather details page. I attempted to retrieve a map from the
API, but was unsuccessful.

Gabe: Coded app routes to each individual page. Took Armando's initial json and request code, and added functionality and test endpoints 
for each individual data dump. Coded the form in home route such that it returned a string that was the user city search input.
Keying, API access and research in these aspects were done by Armando, and I built upon them by looking into json dumps and coding HTML
to display data from the requests. Added longitude and latitude data access directly for convenience.
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
    # Defines the route to homepage, intakes city name via form in html named citytxtbox



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

