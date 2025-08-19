from django.urls import path
from .views import LDOSDeviceListView
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="views/", permanent=True)),
    path("views/", LDOSDeviceListView.as_view(), name="ldos-device-list"),
]

# urlpatterns = [
#     path("", LDOSDeviceListView.as_view(), name="ldos-device-list"),
# ]
