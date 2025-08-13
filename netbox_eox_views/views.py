from datetime import date, datetime
from dcim.models import Device
from dcim.tables import DeviceTable
from utilities.views import ObjectListView


class LDOSDeviceListView(ObjectListView):
    queryset = Device.objects.exclude(custom_fields__ldos_data__isnull=True)
    table = DeviceTable
    template_name = "dcim/device_list.html"  # ✅ use the same template as Devices
    action_buttons = ("add",)  # shows the + Add button

    def get_queryset(self):
        today = date.today()
        devices = super().get_queryset()

        # Filter devices where ldos_data < today
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
