from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dcim.models import Device
from django.db.models import Q
from netbox.views import generic
from .tables import LDOSDeviceTable, ExpiredLicenseDeviceTable
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


class ExpiredLicenseDeviceListView(generic.ObjectListView):
    table = ExpiredLicenseDeviceTable
    template_name = "netbox_eox_views/device_list_expired_license.html"
    action_buttons = ("add", "expiry_year")

    def get_queryset(self, request):
        today = date.today()
        year_from_today_date = today + relativedelta(years=1)
        filter_expiry_year = request.GET.get("expiry_year") == "1"
        expiry_before = request.GET.get("expiry_before")
        if expiry_before:
            try:
                expiry_before_date = datetime.strptime(expiry_before, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                expiry_before_date = None
        else:
            expiry_before_date = None

        devices = Device.objects.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        for device in devices:
            service_contract_end = device.custom_field_data.get("Service Contract End")
            if not service_contract_end:
                continue
            try:
                contract_end_date = datetime.strptime(service_contract_end, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if expiry_before_date:
                if contract_end_date < expiry_before_date:
                    matching_ids.append(device.id)
            elif filter_expiry_year:
                if contract_end_date < year_from_today_date:
                    matching_ids.append(device.id)
            else:
                if contract_end_date < today:
                    matching_ids.append(device.id)
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        return {
            "today": date.today()
        }

    def expiry_year_button(self, request):
        url = f"{reverse('netbox_eox_views:expired_license_device_list')}?expiry_year=1"
        return HttpResponseRedirect(url)

