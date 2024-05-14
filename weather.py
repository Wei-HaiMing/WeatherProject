"""
Authors: Armando, Lily, Eduardo, Gabe
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

    return render_template('Weather_Details.html', city_name = city_name, geodata = geodata, weatherdata = weatherdata)
