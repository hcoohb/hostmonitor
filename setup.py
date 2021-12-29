
# -*- coding: utf-8 -*-
from setuptools import setup

long_description = None
INSTALL_REQUIRES = [
    'paho-mqtt',
    'psutil',
]
ENTRY_POINTS = {
    'console_scripts': [
        'hostmonitor = hostmonitor.hostmonitor:main',
    ],
}

setup_kwargs = {
    'name': 'hostmonitor',
    'version': '0.1',
    'description': 'Python application to monitor sensors and others on the host',
    'long_description': long_description,
    'license': 'MIT',
    'author': '',
    'author_email': 'Fabien Valthier <hcoohb@gmail.com>',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hcoohb/hostmonitor',
    'packages': [
        'hostmonitor.exports',
        'hostmonitor.probes',
    ],
    'package_data': {'': ['*']},
    'install_requires': INSTALL_REQUIRES,
    'python_requires': '>=3.7',
    'entry_points': ENTRY_POINTS,

}


setup(**setup_kwargs)
