import django_tables2 as tables
from dcim.tables import DeviceTable

class LDOSDeviceTable(DeviceTable):
    ldos_data = tables.Column(
        verbose_name="LDOS Date",
        accessor="custom_field_data.ldos_data"
    )

    class Meta(DeviceTable.Meta):
        fields = DeviceTable.Meta.fields + ("ldos_data",)