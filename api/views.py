from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Orders, Vehicles, Drivers
from .serializers import OrdersSerializer, VehiclesSerializer, DriversSerializer, ResponseSerializer
from .services.assign_vehicle_driver import AssignVehicleDriver


# List and create orders
class OrdersListCreate(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


# List and create vehicles
class VehiclesListCreate(generics.ListCreateAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehiclesSerializer


# List and create drivers
class DriversListCreate(generics.ListCreateAPIView):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer


# Assigns the best vehicle and driver for a given order
class SmartVehicleAssignment(APIView):
    """
        API endpoint to assign a vehicle and driver to a given order.
    """
    def post (self, request, order_id):
        """
            POST method to process vehicle assignment for the order.

            Args:
                request (Request): DRF request object
                order_id (int): ID of the order to assign

            Returns:
                Response: Serialized assignment result containing vehicle, driver, distance, cost, and reasoning
        """
        # Initialize the assignment service with the order
        assignment = AssignVehicleDriver(order_id)

        # Get assignment result
        result = assignment.get_assigned_vehicle_driver()

        # Serialize and return the result
        serialized_result = ResponseSerializer(result)
        return Response(serialized_result.data)