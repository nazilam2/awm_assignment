# myapp/serializers.py
from rest_framework import serializers
from .models import GasStation

class GasStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GasStation
        fields = '__all__'  # Include all fields in the model
