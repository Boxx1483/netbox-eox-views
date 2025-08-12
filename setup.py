from setuptools import find_packages, setup

setup(
    name='netbox-eox-views',
    version='0.1',
    description='A NetBox plugin for EOX device filtering',
    install_requires=[],
    packages=find_packages(include=["netbox_eox*"]),
    include_package_data=True,
    zip_safe=False,
)