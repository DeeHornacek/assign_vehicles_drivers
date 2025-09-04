from django.contrib import admin
from .models import Orders, Vehicles, Drivers

# Register models to appear in Django admin
admin.site.register(Orders)
admin.site.register(Vehicles)
admin.site.register(Drivers)