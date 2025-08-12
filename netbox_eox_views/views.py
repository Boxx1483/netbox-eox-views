from datetime import date, datetime
from dcim.models import Device
from django.views.generic import ListView

class LDOSDeviceListView(ListView):
    template_name = "netbox_eox_views/device_ldos_list.html"
    model = Device
    context_object_name = "devices"

    def get_queryset(self):
        today = date.today()
        devices = Device.objects.exclude(custom_fields__ldos_data__isnull=True)

        filtered_devices = []
        for d in devices:
            ldos_value = d.custom_fields.get("ldos_data")
            if not ldos_value:
                continue

            # Convert string date (YYYY-MM-DD) to date object
            try:
                ldos_date = datetime.strptime(ldos_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue  # Skip invalid date formats

            if ldos_date < today:
                filtered_devices.append(d)

        return filtered_devices
