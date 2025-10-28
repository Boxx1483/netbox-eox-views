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
            PluginMenuItem(
                link="plugins:netbox_eox_views:eosv-device-list",
                link_text="End-of-Security-Vulnerabilities",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
        ("SUPPORT & CONTRACTS", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:expired-license-device-list",
                link_text="Expired Service Contracts",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
        ("MISSING DATA", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:missing-data-device-list",
                link_text="Devices with Missing EOX Data",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
            PluginMenuItem(
                link="plugins:netbox_eox_views:missing-data-device-list",
                link_text="Devices with Missing Support Contracts",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
    )
)
