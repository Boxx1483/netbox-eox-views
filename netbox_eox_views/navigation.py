from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton

menu = PluginMenu(
    label="EOX Views",
    icon_class="mdi mdi-sitemap",
    groups=(
        ("Views", (
            PluginMenuItem(
                link="plugins:netbox_eox_views:ldos-device-list",
                link_text="LDOS Devices",
                permissions=["dcim.view_site", "dcim.view_device"],
            ),
        )),
    )
)
