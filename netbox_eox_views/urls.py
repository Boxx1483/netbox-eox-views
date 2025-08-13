from django.urls import path
from .views import LDOSDeviceListView

app_name = "netbox_eox_views"

urlpatterns = [
    path("", LDOSDeviceListView.as_view(), name="ldos-device-list"),
]
