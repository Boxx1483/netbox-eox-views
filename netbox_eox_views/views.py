from datetime import date, datetime
from dcim.models import Device
from netbox.views import generic
from django.db.models import Q
from .tables import LDOSDeviceTable


class LDOSDeviceListView(generic.ObjectListView):
    table = LDOSDeviceTable
    template_name = "dcim/device_list.html"
    action_buttons = ("add",)

    def get_queryset(self, request):
        today = date.today()
        devices = Device.objects.exclude(custom_field_data__ldos_data__isnull=True)
        matching_ids = []
        for device in devices:
            ldos_value = device.custom_field_data.get("ldos_data")
            if not ldos_value:
                continue
            try:
                ldos_date = datetime.strptime(ldos_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if ldos_date < today:
                matching_ids.append(device.id)

        return Device.objects.filter(id__in=matching_ids)

