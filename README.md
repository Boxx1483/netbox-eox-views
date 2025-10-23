# netbox-eox-views
hh
**netbox-eox-views** is a NetBox 4.x plugin for managing and displaying End-of-Life (EoX) information for devices.  
It provides custom views and navigation for tracking device lifecycle status within NetBox.

## Features

- List devices with EoX information
- Custom navigation integration
- Redirects and custom views for device lifecycle management

## Requirements

- NetBox 4.x
- Python 3.8+
- Django (compatible with NetBox 4.x)

## Installation

1. Clone this repository into your NetBox `plugins` directory:

    ```sh
    git clone https://github.com/boxx1483/netbox-eox-views.git
    ```

2. Add `'netbox_eox_views'` to the `PLUGINS` list in your NetBox `configuration.py`:

    ```python
    PLUGINS = [
        'netbox_eox_views',
    ]
    ```

3. Restart NetBox.

## Usage

- Access the EoX device list at `/plugins/netbox_eox_views/ldos-device-list/`
- The plugin adds navigation entries and custom views for device lifecycle management.

## File Structure

- `netbox_eox_views/urls.py` – URL routing for plugin views
- `netbox_eox_views/views.py` – View classes (e.g., `LDOSDeviceListView`)
- `netbox_eox_views/navigation.py` – Custom navigation integration

## License

This project is licensed under the GNU General Public License v2.0. See [LICENSE](LICENSE) for details.

## Author

Bo Mikkelsen / Netic A/S
