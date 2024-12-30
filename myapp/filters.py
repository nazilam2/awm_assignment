from django_filters import rest_framework as filters
from .models import GasStation
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D  # For geospatial distance filtering

class GasStationFilter(filters.FilterSet):
    # A filter to search gas stations by name (case-insensitive)
    name = filters.CharFilter(lookup_expr='icontains', label='Name')

    # A filter to search by the location (filtering gas stations within a given point)
    location = filters.CharFilter(method='filter_by_location', label='Location')

    # A filter to filter by current price (greater than, less than, or equal to)
    min_price = filters.NumberFilter(field_name="current_price", lookup_expr='gte', label='Minimum Price')
    max_price = filters.NumberFilter(field_name="current_price", lookup_expr='lte', label='Maximum Price')

    # A filter to search by rating (greater than, less than, or equal to)
    min_rating = filters.NumberFilter(field_name="user_rating", lookup_expr='gte', label='Minimum Rating')
    max_rating = filters.NumberFilter(field_name="user_rating", lookup_expr='lte', label='Maximum Rating')

    class Meta:
        model = GasStation
        fields = ['name', 'location', 'min_price', 'max_price', 'min_rating', 'max_rating']

    def filter_by_location(self, queryset, name, value):
        """
        This method filters the queryset to find GasStation locations
        within a given point.
        
        Example query parameter:
        ?location=longitude,latitude
        """
        try:
            # Assuming `value` is passed as "longitude,latitude" string
            lon, lat = map(float, value.split(','))
            point = Point(lon, lat, srid=4326)
            # You can specify a distance for the proximity filter here (e.g., 5km radius)
            return queryset.filter(location__distance_lte=(point, D(km=5)))
        except ValueError:
            return queryset  # If the value is incorrect or missing, return all results.
