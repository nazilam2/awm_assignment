from django.contrib import admin
from .models import GasStation
from .models import GasStation, FavoriteStation, StationHistory

class GasStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'current_price', 'user_rating', 'reviews')  # Removed 'created_at' and 'updated_at'

    search_fields = ('name', 'address', 'current_price', 'user_rating')  # Allow searching by name, address, price, and rating
    list_filter = ('user_rating', 'current_price')  # Filters by user rating and price
    ordering = ('name',)  # Default ordering by name


# FavoriteStation Admin
class FavoriteStationAdmin(admin.ModelAdmin):
    list_display = ('user', 'gas_station')  # Display user and gas station
    search_fields = ('user__username', 'gas_station__name')  # Search by user and gas station name
    list_filter = ('user',)  # Filter by user
    ordering = ('user',)  # Default ordering by user

# StationHistory Admin
class StationHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'gas_station', 'timestamp')  # Display user, gas station, and timestamp
    search_fields = ('user__username', 'gas_station__name')  # Search by user and gas station name
    list_filter = ('timestamp',)  # Filter by timestamp
    ordering = ('-timestamp',)  # Default ordering by timestamp (most recent first)

# Register the models with the admin site

admin.site.register(FavoriteStation, FavoriteStationAdmin)
admin.site.register(StationHistory, StationHistoryAdmin)
admin.site.register(GasStation, GasStationAdmin)
