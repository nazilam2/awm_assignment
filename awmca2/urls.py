# urls.py
from django.contrib import admin
from django.urls import include, path
from myapp.views import home  # Import the home view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home, name='home'),  # Root URL mapped to the home view
    path('api/v1/', include('myapp.urls')),  # Include your app's URLs
    path('', include('pwa.urls')),  # Make sure this is placed after your root URL
    path('frontend/', include('frontend.urls')),
]
