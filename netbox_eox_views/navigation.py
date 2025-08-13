from extras.plugins import PluginMenu, PluginMenuItem

menu = PluginMenu(
    label="EOX Views",
    groups=(
        ("Views", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:ldos-device-list",
                link_text="LDOS Devices"
            ),
        )),
    )
)
