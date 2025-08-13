from extras.plugins import PluginConfig

class NetBoxEOXViewsConfig(PluginConfig):
    name = "netbox_eox_views"
    verbose_name = "EOX Device Views"
    description = "Lists devices with LDOS date before today"
    version = "0.1"
    author = "Your Name"
    author_email = "you@example.com"
    base_url = "eox-views"
    urls = "netbox_eox_views.urls"  # ✅ Required for routing

config = NetBoxEOXViewsConfig
