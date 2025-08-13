from datetime import date, datetime
from dcim.models import Device
from netbox.views import generic
from .tables import LDOSDeviceTable


class LDOSDeviceListView(generic.ObjectListView):
    table = LDOSDeviceTable
    template_name = "dcim/device_list.html"
    action_buttons = ("add",)

    def get_queryset(self):
        today = date.today()
        devices = Device.objects.exclude(custom_fields__ldos_data__isnull=True)

        filtered_devices = []
        for device in devices:
            ldos_value = device.custom_fields.get("ldos_data")
            if not ldos_value:
                continue
            try:
                ldos_date = datetime.strptime(ldos_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if ldos_date < today:
                filtered_devices.append(device)

        return filtered_devices
