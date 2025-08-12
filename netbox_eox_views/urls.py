from django.urls import path
from .views import LDOSDeviceListView

urlpatterns = [
    path("", LDOSDeviceListView.as_view(), name="ldos-device-list"),
]
