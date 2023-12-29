from django.shortcuts import render, redirect
from django.contrib import messages
import requests
from .models import City
from .forms import CityForm
from datetime import datetime
# Create your views here.

def index(request):
    cities = City.objects.all()
    
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=1d99da292ee1903a4b82bd6ef7ee21d1"
    if request.method == "POST":
        name = request.POST.get("name")
        name = name.title()
        if not City.objects.filter(name = name).exists():
            City.objects.create(
                name = name
            )
        
    
    form = CityForm()

    weather_data = []
    if len(cities) > 0:
        for city in cities:
            city_weather = requests.get(url.format(city)).json()

            now = datetime.now()
            current_time = now.strftime("%H:%M")

            try:
                weather = {
                    'id' : city.id,
                    'city' : city,
                    "temprature" : city_weather['main']['temp'],
                    "temprature_max" : city_weather['main']['temp_max'],
                    "temprature_min" : city_weather['main']['temp_min'],
                    'description' : city_weather['weather'][0]['description'],
                    'main' : city_weather['weather'][0]['main'],
                    'icon' : city_weather['weather'][0]['icon'],
                    'humidity': city_weather['main']['humidity'],
                    'pressure' : city_weather['main']['pressure'],
                    'windspeed' : city_weather['wind']['speed'],
                    'time': current_time
                }
                weather_data.append(weather)
            except:
                messages.error(request, "City Does not exists")
                City.objects.filter(name = city.name).delete()

    cities = City.objects.all()
    # City.objects.all().delete()
    context = {'weather_data':weather_data, 'form':form, 'cities':cities}
    return render(request, "index.html", context)

# def onecity(request, id):
#     return render(request, "onecity.html", context={'weather': data})