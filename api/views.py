from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Orders, Vehicles, Drivers
from .serializers import OrdersSerializer, VehiclesSerializer, DriversSerializer, ResponseSerializer
from .services.assign_vehicle_driver import AssignVehicleDriver


# CRUD cez router
class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class VehiclesViewSet(viewsets.ModelViewSet):
    queryset = Vehicles.objects.all()
    serializer_class = VehiclesSerializer


class DriversViewSet(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriversSerializer


# Smart Vehicle Assignment endpoint
class SmartVehicleAssignment(APIView):
    """
    API endpoint to assign a vehicle and driver to a given order.
    """
    def post(self, request, order_id):
        assignment = AssignVehicleDriver(order_id)
        result = assignment.get_assigned_vehicle_driver()
        serialized_result = ResponseSerializer(result)
        return Response(serialized_result.data)
