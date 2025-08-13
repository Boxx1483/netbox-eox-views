from netbox.plugins import PluginConfig

class NetBoxEOXViewsConfig(PluginConfig):
    name = "netbox_eox_views"
    verbose_name = "EOX Device Filter"
    description = "Lists devices with EOX date before today"
    version = "0.1"
    author = "Bo Mikkelsen"
    author_email = "bom@netic.dk"
    base_url = "eox-views"
    urls = "netbox_eox_views.urls"

config = NetBoxEOXViewsConfig