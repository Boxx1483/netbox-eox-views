from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dcim.models import Device
from django.db.models import Q
from netbox.views import generic
from .tables import LDOSDeviceTable, ExpiredLicenseDeviceTable, EOSVDeviceTable, MissingDataDeviceTable
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


class EOSVDeviceListView(generic.ObjectListView):
    table = EOSVDeviceTable
    template_name = "netbox_eox_views/device_list_ldos.html"  # Using same template for now
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
            eosv_value = device.custom_field_data.get("eosv_data")
            if not eosv_value:
                continue
            try:
                eosv_date = datetime.strptime(eosv_value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                continue
            if ldos_before_date:
                if eosv_date < ldos_before_date:
                    matching_ids.append(device.id)
            elif filter_ldos_year:
                if eosv_date < year_from_today_date:
                    matching_ids.append(device.id)
            else:
                if eosv_date < today:
                    matching_ids.append(device.id)
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        return {
            "today": date.today()
        }

    def ldos_year_button(self, request):
        url = f"{reverse('netbox_eox_views:eosv_device_list')}?ldos_year=1"
        return HttpResponseRedirect(url)


class MissingEoxDataDeviceListView(generic.ObjectListView):
    table = MissingDataDeviceTable
    template_name = "netbox_eox_views/device_list_ldos.html"
    action_buttons = ("add",)

    def get_queryset(self, request):
        devices = Device.objects.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        
        for device in devices:
            has_eos_data = device.custom_field_data.get("eos_data")
            has_eosr_data = device.custom_field_data.get("eosr_data")
            has_eosv_data = device.custom_field_data.get("eosv_data")
            has_ldos_data = device.custom_field_data.get("ldos_data")
            
            if not has_eos_data or not has_eosr_data or not has_eosv_data or not has_ldos_data:
                matching_ids.append(device.id)
                
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        return {
            "today": date.today()
        }


class MissingContractDeviceListView(generic.ObjectListView):
    table = MissingDataDeviceTable
    template_name = "netbox_eox_views/device_list_ldos.html"
    action_buttons = ("add",)

    def get_queryset(self, request):
        devices = Device.objects.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        
        for device in devices:
            has_contract_end = device.custom_field_data.get("Service Contract End")
            has_contract_status = device.custom_field_data.get("service_contract_status")
            
            if not has_contract_end or not has_contract_status:
                matching_ids.append(device.id)
                
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        return {
            "today": date.today()
        }

