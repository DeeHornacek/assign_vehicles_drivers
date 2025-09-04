from rest_framework import serializers
from .models import Orders, Vehicles, Drivers


# Serializer for Orders model - includes all fields
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


# Serializer for Vehicles model - includes all fields
class VehiclesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicles
        fields = '__all__'


# Serializer for Drivers model - includes all fields
class DriversSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'


# Serializer for response, custom dict
class ResponseSerializer(serializers.Serializer):
    assigned_vehicle = serializers.CharField(max_length=100)
    assigned_driver = serializers.CharField(max_length=100)
    estimated_cost = serializers.FloatField()
    distance_km = serializers.FloatField()
    reasoning = serializers.CharField()