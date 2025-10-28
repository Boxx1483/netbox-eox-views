from django.urls import path
from .views import LDOSDeviceListView, ExpiredLicenseDeviceListView, EOSVDeviceListView, MissingEoxDataDeviceListView, MissingContractDeviceListView
from django.views.generic import RedirectView

app_name = "netbox_eox_views"

urlpatterns = [
    path("", RedirectView.as_view(url="views/", permanent=True)),
    path("ldos-device-list/", LDOSDeviceListView.as_view(), name="ldos-device-list"),
    path("expired-license-device-list/", ExpiredLicenseDeviceListView.as_view(), name="expired-license-device-list"),
    path("eosv-device-list/", EOSVDeviceListView.as_view(), name="eosv-device-list"),
    path("missing-data-device-list/", MissingEoxDataDeviceListView.as_view(), name="missing-eox-data-device-list"),
    path("missing-contract-device-list/", MissingContractDeviceListView.as_view(), name="missing-contract-device-list"),
]
