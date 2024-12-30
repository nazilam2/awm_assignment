# myapp/urls.py
# myapp/urls.py
from django.urls import path
from .views import GasStationListCreateView, ListCreateGasStationView, GasStationRetrieveUpdateDestroyView, search_gas_stations
from django.urls import path
from .views import register_view, login_view, logout_view
from . import views

# urlpatterns = [
#     path('search/', search_gas_stations, name='search_gas_stations'),
#    # path('gasstations/', ListCreateGasStationView.as_view(), name='gasstation-list'),
#     path('gasstations/', GasStationListCreateView.as_view(), name='gasstation-list'),
#     path('gasstations/<str:pk>/', GasStationRetrieveUpdateDestroyView.as_view(), name='gasstation-detail'),
# ]

urlpatterns = [
    path('search/', search_gas_stations, name='search_gas_stations'),
    path('gasstations/', GasStationListCreateView.as_view(), name='gasstation-list'),
    path('gasstations/<str:pk>/', GasStationRetrieveUpdateDestroyView.as_view(), name='gasstation-detail'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # this is for save gast stations 
    path('favorites/', views.view_favorites, name='view_favorites'),
    path('history/', views.view_history, name='view_history'),
    # path('add-to-favorites/<int:station_id>/', views.add_to_favorites, name='add-to-favorites'),
    path('add-to-favorites/<int:station_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:station_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('save_to_history/<int:station_id>/', views.save_to_history, name='save_to_history'),
    
    path('profile/', views.user_profile, name='user_profile'),  # Profile page
    path('api/v1/profile/', views.api_profile, name='api_profile'),
]


