from datetime import date, datetime
from dcim.models import Device
from netbox.views import generic
from .tables import LDOSDeviceTable


class LDOSDeviceListView(generic.ObjectListView):
    table = LDOSDeviceTable
    template_name = "dcim/device_list.html"
    action_buttons = ("add",)

    def get_queryset(self, request):
        today = date.today()
        devices = Device.objects.exclude() # No exclude filter applied, because custom fields cannot be used in the queryset directly. Perhaps put state=production or similar.

        filtered_devices = []
        for device in devices:
            ldos_value = device.custom_field_data.get("ldos_data")
            if not ldos_value:
                continue
            try:
                ldos_date = datetime.strptime(ldos_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if ldos_date < today:
                filtered_devices.append(device)

        return filtered_devices
