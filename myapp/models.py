from django.contrib.gis.db import models
from django.contrib.auth.models import User

class GasStation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user_rating = models.FloatField(null=True)
    reviews = models.TextField(blank=True)
    location = models.PointField(null=True)  # Spatial Field for location (longitude, latitude)

    def __str__(self):
        return self.name

class FavoriteStation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'gas_station')

    def __str__(self):
        return f'{self.user.username} - {self.gas_station.name}'


class StationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gas_station = models.ForeignKey(GasStation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.gas_station.name} at {self.timestamp}'