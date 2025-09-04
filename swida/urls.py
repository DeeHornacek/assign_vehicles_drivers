"""
URL configuration for assign_vehicles_drivers project.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import OrdersViewSet, VehiclesViewSet, DriversViewSet, SmartVehicleAssignment

router = DefaultRouter()
router.register(r'api/orders', OrdersViewSet)
router.register(r'api/vehicles', VehiclesViewSet)
router.register(r'api/drivers', DriversViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/orders/<int:order_id>/assign-optimal-vehicle/', SmartVehicleAssignment.as_view(), name='assign-optimal-vehicle'),
]

