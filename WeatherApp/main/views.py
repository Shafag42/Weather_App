from django.shortcuts import render,redirect
import requests
from .models import City
from .forms import CityForm

# Create your views here.

def index(request):  # sourcery skip: useless-else-on-loop
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=871f58e0f5cacfb1b363ee1f49d817c5'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'

    # if request.method == 'POST':
    #     form = CityForm(request.POST)
    #     form.save()

    form = CityForm
    weather_news = []

    for city in cities:
        # city_weather = requests.get(url.format(city)).json()
        response = requests.get(url.format(city.name))

        if response.status_code == 200:

            city_weather = response.json()
        
            weather = {
                'city': city.name,
                'temperature': city_weather['main']['temp'],
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
                'humidity': city_weather['main']['humidity'],
                'pressure': city_weather['main']['pressure'],
                'country': city_weather['sys']['country'],
                'sunrise': city_weather['sys']['sunrise'],
                'sunset': city_weather['sys']['sunset'],
                'windspeed': city_weather['wind']['speed']
            }

            weather_news.append(weather)
    else: 
     form = CityForm()

    context = {'weather_news': weather_news, 'form': form}

    return render(request, 'index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('home')