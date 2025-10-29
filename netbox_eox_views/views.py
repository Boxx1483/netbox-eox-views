from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from dcim.models import Device
from django.db.models import Q
from netbox.views import generic
from .tables import LDOSDeviceTable, ExpiredLicenseDeviceTable, EOSVDeviceTable, MissingDataDeviceTable
from django.urls import reverse
from django.http import HttpResponseRedirect
from dcim.filtersets import DeviceFilterSet
try:
    from .forms import MissingDataDeviceFilterForm
except ImportError:
    MissingDataDeviceFilterForm = None


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
            service_contract_status = device.custom_field_data.get("service_contract_status")
            
            if service_contract_status == "Expired":
                matching_ids.append(device.id)
                continue
            
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
    queryset = Device.objects.all()
    table = MissingDataDeviceTable
    template_name = "netbox_eox_views/device_list_missing_data.html"
    action_buttons = ("add", "export")
    filterset = DeviceFilterSet
    # filterset_form - temporarily disabled to fix container startup
    # Will be enabled once we verify the import works in your NetBox version
    
    def get_queryset(self, request):
        # Let the parent apply filterset filters first
        base_queryset = super().get_queryset(request)
        
        devices = base_queryset.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        
        missing_field = request.GET.get("missing_field", "")
        
        for device in devices:
            if missing_field == "eos":
                has_data = device.custom_field_data.get("eos_data")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "eosr":
                has_data = device.custom_field_data.get("eosr_data")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "eosv":
                has_data = device.custom_field_data.get("eosv_data")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "ldos":
                has_data = device.custom_field_data.get("ldos_data")
                if not has_data:
                    matching_ids.append(device.id)
            else:
                eos_data = device.custom_field_data.get("eos_data")
                eosr_data = device.custom_field_data.get("eosr_data")
                eosv_data = device.custom_field_data.get("eosv_data")
                ldos_data = device.custom_field_data.get("ldos_data")
                
                if not eos_data and not eosr_data and not eosv_data and not ldos_data:
                    matching_ids.append(device.id)
                
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        missing_field = request.GET.get("missing_field", "")
        field_names = {
            "eos": "EOS Data",
            "eosr": "EOSR Data",
            "eosv": "EOSV Data",
            "ldos": "LDOS Data"
        }
        title = f"Devices with Missing {field_names.get(missing_field, 'EOX Data')}"
        
        filter_options = [
            ("eos", "Missing EOS"),
            ("eosr", "Missing EOSR"),
            ("eosv", "Missing EOSV"),
            ("ldos", "Missing LDOS")
        ]
        
        return {
            "today": date.today(),
            "view_title": title,
            "current_filter": missing_field,
            "filter_options": filter_options
        }


class MissingContractDeviceListView(generic.ObjectListView):
    queryset = Device.objects.all()
    table = MissingDataDeviceTable
    template_name = "netbox_eox_views/device_list_missing_data.html"
    action_buttons = ("add", "export")
    filterset = DeviceFilterSet
    # filterset_form - temporarily disabled to fix container startup
    # Will be enabled once we verify the import works in your NetBox version

    def get_queryset(self, request):
        base_queryset = super().get_queryset(request)
        
        devices = base_queryset.filter(Q(status="active") | Q(status="production"))
        matching_ids = []
        
        missing_field = request.GET.get("missing_field", "")
        
        for device in devices:
            if missing_field == "end_date":
                has_data = device.custom_field_data.get("Service Contract End")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "status":
                has_data = device.custom_field_data.get("service_contract_status")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "contract_number":
                has_data = device.custom_field_data.get("Service Contract Number")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "service_level":
                has_data = device.custom_field_data.get("Service Contract Service Level")
                if not has_data:
                    matching_ids.append(device.id)
            elif missing_field == "contract_start":
                has_data = device.custom_field_data.get("Service Contract Start")
                if not has_data:
                    matching_ids.append(device.id)
            else:
                contract_end = device.custom_field_data.get("Service Contract End")
                contract_status = device.custom_field_data.get("service_contract_status")
                contract_number = device.custom_field_data.get("Service Contract Number")
                contract_service_level = device.custom_field_data.get("Service Contract Service Level")
                contract_start = device.custom_field_data.get("Service Contract Start")
                
                if (not contract_end and not contract_status and not contract_number 
                    and not contract_service_level and not contract_start):
                    matching_ids.append(device.id)
                
        return Device.objects.filter(id__in=matching_ids)

    def get_extra_context(self, request):
        missing_field = request.GET.get("missing_field", "")
        field_names = {
            "end_date": "Contract End Date",
            "status": "Contract Status",
            "contract_number": "Contract Number",
            "service_level": "Contract Service Level",
            "contract_start": "Contract Start Date"
        }
        title = f"Devices with Missing {field_names.get(missing_field, 'Support Contract Data')}"
        
        filter_options = [
            ("end_date", "Missing End Date"),
            ("status", "Missing Status"),
            ("contract_number", "Missing Contract Number"),
            ("service_level", "Missing Service Level"),
            ("contract_start", "Missing Start Date")
        ]
        
        return {
            "today": date.today(),
            "view_title": title,
            "current_filter": missing_field,
            "filter_options": filter_options
        }

