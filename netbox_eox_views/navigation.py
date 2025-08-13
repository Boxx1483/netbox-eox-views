from extras.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_eox_views:ldos-device-list",  # matches `name=` in urls.py
        link_text="LDOS Devices",
        buttons=()
    ),
)
