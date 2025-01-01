from django.shortcuts import render

# Create your views here.
# gas_station_frontend/views.py

from django.shortcuts import render
import requests

def index(request):
    # Make a GET request to the REST API to fetch gas station data
    response = requests.get('http://127.0.0.1:8000/api/v1/gasstations/')  # Use your actual endpoint here
    #response = requests.get('https://gas-station-finder-app-80f702109b4d.herokuapp.com/api/v1/gasstations/')  # Heroku production URL

    gas_stations = response.json()  # Parse the JSON response

    # Pass the data to the template
    return render(request, 'index.html', {'gas_stations': gas_stations})
