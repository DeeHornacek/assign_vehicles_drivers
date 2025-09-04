from . import views

from django.urls import path

urlpatterns = [
    # Orders endpoints: list and create
    path('api/orders', views.OrdersListCreate.as_view(), name='orders-list-create'),

    # Vehicles endpoints: list and create
    path('api/vehicles', views.VehiclesListCreate.as_view(), name='vehicles-list-create'),

    # Drivers endpoints: list and create
    path('api/drivers', views.DriversListCreate.as_view(), name='drivers-list-create'),

    # Endpoint to assign the optimal vehicle and driver for a specific order
    path(
        'api/orders/<int:order_id>/assign-optimal-vehicle/',
        views.SmartVehicleAssignment.as_view(),
        name='assign-optimal-vehicle'
    ),
]