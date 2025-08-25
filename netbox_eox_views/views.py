from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dcim.models import Device
from django.db.models import Q
from netbox.views import generic
from .tables import LDOSDeviceTable
from django.urls import reverse
from django.http import HttpResponseRedirect


class LDOSDeviceListView(generic.ObjectListView):
    table = LDOSDeviceTable
    template_name = "netbox_eox_views/device_list_ldos.html"
    action_buttons = ("add", "ldos_year")

    def get_queryset(self, request):
        today = date.today()
        year_from_today_date = today + relativedelta(years=1)
        filter_ldos_year = request.GET.get("ldos_year") == "1"
        ldos_before = request.GET.get("ldos_before")
        if ldos_before:
            try:
                ldos_before_date = datetime.strptime(ldos_before, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                ldos_before_date = None
        else:
            ldos_before_date = None

        devices = Device.objects.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        for device in devices:
            ldos_value = device.custom_field_data.get("ldos_data")
            if not ldos_value:
                continue
            try:
                ldos_date = datetime.strptime(ldos_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if ldos_before_date:
                if ldos_date < ldos_before_date:
                    matching_ids.append(device.id)
            elif filter_ldos_year:
                if ldos_date < year_from_today_date:
                    matching_ids.append(device.id)
            else:
                if ldos_date < today:
                    matching_ids.append(device.id)
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        return {
            "today": date.today()
        }

    def ldos_year_button(self, request):
        url = f"{reverse('netbox_eox_views:ldosdevice_list')}?ldos_year=1"
        return HttpResponseRedirect(url)

