from netbox.plugins import PluginMenu, PluginMenuItem

menu = PluginMenu(
    label="Device Lifecycle",
    icon_class="mdi mdi-timer-sand",
    groups=(
        ("END-OF-LIFE", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:ldos-device-list",
                link_text="End-of-Life Devices",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
        ("LICENSING", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:expired-license-device-list",
                link_text="Expired Licenses",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
    )
)
