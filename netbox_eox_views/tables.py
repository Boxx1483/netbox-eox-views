import django_tables2 as tables
from dcim.tables import DeviceTable

class LDOSDeviceTable(DeviceTable):
    ldos_data = tables.Column(
        verbose_name="LDOS Date",
        accessor="custom_field_data.ldos_data"
    )

    class Meta(DeviceTable.Meta):
        fields = DeviceTable.Meta.fields + ("ldos_data",)


class ExpiredLicenseDeviceTable(DeviceTable):
    service_contract_end = tables.Column(
        verbose_name="Service Contract End",
        accessor="custom_field_data.Service Contract End"
    )
    service_contract_status = tables.Column(
        verbose_name="Service Contract Status",
        accessor="custom_field_data.service_contract_status"
    )

    class Meta(DeviceTable.Meta):
        fields = DeviceTable.Meta.fields + ("service_contract_end", "service_contract_status")


class EOSVDeviceTable(DeviceTable):
    eosv_data = tables.Column(
        verbose_name="EOSV Date",
        accessor="custom_field_data.eosv_data"
    )

    class Meta(DeviceTable.Meta):
        fields = DeviceTable.Meta.fields + ("eosv_data",)