from django.urls import path
from .views import LDOSDeviceListView, ExpiredLicenseDeviceListView
from django.views.generic import RedirectView

app_name = "netbox_eox_views"

urlpatterns = [
    path("", RedirectView.as_view(url="views/", permanent=True)),
    path("ldos-device-list/", LDOSDeviceListView.as_view(), name="ldos-device-list"),
    path("expired-license-device-list/", ExpiredLicenseDeviceListView.as_view(), name="expired-license-device-list"),
]
