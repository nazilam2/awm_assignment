from django import forms
from django.shortcuts import render
from rest_framework import generics
from .models import GasStation
from .serializers import GasStationSerializer
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
import time
import logging
from django_filters.rest_framework import DjangoFilterBackend
from .filters import GasStationFilter  # Make sure this filter exists or define it
from rest_framework_gis.pagination import GeoJsonPagination
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.shortcuts import render, redirect

from math import radians, sin, cos, sqrt, atan2

from django.shortcuts import get_object_or_404, render, redirect
from .models import GasStation, FavoriteStation, StationHistory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import GasStation, FavoriteStation
#from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base.html')  # or base.html or any other template you're using
logger = logging.getLogger(__name__)

# this is for the filter 
class GasStationListCreateView(generics.ListCreateAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GasStationFilter
    pagination_class = GeoJsonPagination  # Optional: for paginating geospatial data
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply additional filtering here, if needed
        return queryset
    
# List and Create view for GasStation model
class ListCreateGasStationView(generics.ListCreateAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationSerializer

# Retrieve, Update, and Destroy view for a specific GasStation
class GasStationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = GasStation.objects.all()
    serializer_class = GasStationSerializer

# Form for searching gas stations
class GasStationSearchForm(forms.Form):
    address = forms.CharField(label='Enter Address or Location', max_length=255)

# Retry geocoding with delay for certain errors
def geocode_with_retry(geolocator, address, retries=3, delay=2, timeout=10):
    for attempt in range(retries):
        try:
            return geolocator.geocode(address, timeout=timeout)  # Increased timeout for better reliability
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timed out for address: {address}. Attempt {attempt + 1}.")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise Exception("Geocoding service timed out after multiple attempts.")
        except GeocoderServiceError as e:
            logger.error(f"Geocoder service error: {str(e)}")
            if "500" in str(e):
                if attempt < retries - 1:
                    time.sleep(delay)  # Retry after delay
                    continue  # Retry the request
                else:
                    raise Exception("Geocoding service returned an internal server error after multiple attempts.")
            else:
                raise Exception(f"Geocoding service error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during geocoding: {str(e)}")
            raise Exception(f"An unexpected error occurred: {str(e)}")

# Handle errors during geocoding
def handle_geocoding_error(e, form):
    if isinstance(e, GeocoderServiceError):
        form.add_error('address', 'The geocoding service is currently unavailable. Please try again later.')
    elif isinstance(e, GeocoderTimedOut):
        form.add_error('address', 'The geocoding request timed out. Please try again.')
    else:
        form.add_error('address', f'An unexpected error occurred during geocoding: {str(e)}')

# Haversine function to calculate distance
def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    return R * c


# View to handle gas station search
def search_gas_stations(request):
    results = []
    user_location = None
    favorites = []  # Default to an empty list for anonymous users

    if request.user.is_authenticated:
        favorites = FavoriteStation.objects.filter(user=request.user).values_list('gas_station_id', flat=True)

    if request.method == 'POST':
        print("Form data:", request.POST)  # Debugging: Print form data to see what was submitted
        form = GasStationSearchForm(request.POST)

        if form.is_valid():
            print("Form is valid")
            address = form.cleaned_data.get('address')
            station_name = form.cleaned_data.get('station_name')

            print(f"Address: {address}")
            print(f"Station Name: {station_name}")  # Added this to debug station_name value

            # Geocoding to get user's latitude and longitude
            geolocator = Nominatim(user_agent="gas_station_locator")
            try:
                location = geocode_with_retry(geolocator, address)
                if location:
                    user_location = (location.latitude, location.longitude)
                    user_point = Point(location.longitude, location.latitude, srid=4326)

                    # GIS-based query: Filtering within 5km radius
                    queryset = GasStation.objects.annotate(distance=Distance('location', user_point))

                    # Filter by station name if provided
                    if station_name:
                        print(f"Applying filter for station name: {station_name}")  # Debugging filter logic
                        queryset = queryset.filter(name__icontains=station_name)

                    # Filter stations within 5km radius
                    queryset = queryset.filter(distance__lte=D(km=5)).order_by('distance')

                    # Debugging: Check if queryset is returning results
                    print(f"Filtered queryset: {queryset}")

                    stations = queryset.all()

                    # Calculate and assign distance to each station
                    for station in stations:
                        distance = haversine_distance(user_location[0], user_location[1], station.location.y, station.location.x)
                        station.distance = distance

                    # Sort stations by calculated distance
                    results = sorted(stations, key=lambda x: x.distance)

                else:
                    form.add_error('address', 'Could not geocode the address. Please try another one.')

            except (GeocoderServiceError, GeocoderTimedOut) as e:
                form.add_error('address', 'Geocoding service error. Please try again later.')
            except Exception as e:
                form.add_error('address', f'An unexpected error occurred: {str(e)}')

        else:
            print("Form is not valid:", form.errors)  # Print form errors for debugging

    return render(request, 'base.html', {
        'form': form,
        'results': results,
        'user_location': user_location,
        'favorites': favorites
    })


# This is for login/logout 
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful registration
            return redirect('home')  # Redirect to homepage or any desired page
        else:
            print(form.errors)  # Debugging: Print form errors to the console
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to homepage or dashboard
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to homepage or login page after logout

# save to faviorate 
def add_to_favorites(request, station_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            station = GasStation.objects.get(id=station_id)
            FavoriteStation.objects.create(user=request.user, gas_station=station)
            return JsonResponse({'message': 'Added to Favorites'}, status=200)
        except GasStation.DoesNotExist:
            logger.error(f"GasStation with ID {station_id} not found.")
            return JsonResponse({'message': 'Station not found'}, status=404)
        except Exception as e:
            logger.error(f"Error adding to favorites: {e}")
            return JsonResponse({'message': 'An error occurred.'}, status=500)
    else:
        logger.warning("Unauthorized or invalid method.")
        return JsonResponse({'message': 'Unauthorized'}, status=401)

def remove_from_favorites(request, station_id):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            # Get the gas station
            station = GasStation.objects.get(id=station_id)
            
            # Remove from user's favorites
            FavoriteStation.objects.filter(user=request.user, gas_station=station).delete()

            return JsonResponse({'message': 'Removed from Favorites'}, status=200)
        except GasStation.DoesNotExist:
            return JsonResponse({'message': 'Station not found'}, status=404)
    else:
        return JsonResponse({'message': 'Unauthorized'}, status=401)



@login_required
def view_favorites(request):
    favorites = FavoriteStation.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'favorites': favorites})


@login_required
def save_to_history(request, station_id):
    station = get_object_or_404(GasStation, pk=station_id)
    StationHistory.objects.create(user=request.user, gas_station=station)
    return JsonResponse({"message": "Saved to history!"})


@login_required
def view_history(request):
    history = StationHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'history.html', {'history': history})

@login_required
def user_profile(request):
    # Get the user's favorite gas stations
    favorites = FavoriteStation.objects.filter(user=request.user)

    # To get the full details of the stations in favorites
    favorite_stations = []
    for favorite in favorites:
        station = GasStation.objects.get(id=favorite.gas_station.id)  # Corrected to 'gas_station'
        favorite_stations.append(station)

    # History could also be implemented similarly
    history = StationHistory.objects.filter(user=request.user)  # Use 'StationHistory' here

    return render(request, 'profile.html', {
        'favorites': favorite_stations,
        'history': history,
    })


@login_required
def api_profile(request):
    """
    This view will return the user's profile data in JSON format.
    """
    user_data = {
        'username': request.user.username,
        'email': request.user.email,
        # Add any additional profile data here, such as favorites, history, etc.
    }
    return JsonResponse(user_data)