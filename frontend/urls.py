# gas_station_frontend/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Display the list of gas stations
]
