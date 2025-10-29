from dcim.forms import DeviceFilterForm


class MissingDataDeviceFilterForm(DeviceFilterForm):
    """
    Custom filter form for Missing Data Device views.
    Focuses on key device fields like manufacturer.
    """
    
    class Meta(DeviceFilterForm.Meta):
        fields = [
            'q',
            'manufacturer_id',
            'device_type_id',
            'site_id',
            'status',
        ]
        labels = {
            'manufacturer_id': 'Manufacturer',
            'device_type_id': 'Device Type',
            'site_id': 'Site',
            'status': 'Status',
        }

