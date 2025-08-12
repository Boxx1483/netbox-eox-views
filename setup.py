from setuptools import find_packages, setup

setup(
    name='netbox_eox_views',
    version='0.1',
    description='A NetBox plugin for EOX device filtering',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)