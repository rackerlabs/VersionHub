#!/usr/bin/env python

import sys
from os.path import dirname

import paver.doctools
from paver.easy import options
from paver.setuputils import setup, find_packages

# make sure the current directory is in the python import path
sys.path.append(dirname(__file__))

# default task options
options(root_dir=dirname(__file__))

# import our tasks
from task.tests import *
from task.virtualenv import *

#
# project dependencies
#

install_requires = [
    'cerberus',
    'coverage==3.6',
    'motor',
    'python-dateutil',
    'python3-memcached',
    'pytz',
    'pyyaml==3.10',
    'tornado==3.1',
]

#
# Setuptools configuration, used to create python .eggs and such.
# See: http://bashelton.com/2009/04/setuptools-tutorial/ for a nice
# setuptools tutorial.
#

setup(
    name="version_hub",
    version="0.1",

    # packaging infos
    package_data={'': ['*.yaml', '*.html', '*.css', '*.js']},
    packages=find_packages(exclude=['test', 'test.*']),

    # dependency infos
    install_requires=install_requires,

    entry_points={
        'console_scripts': [
            'version_hub = application:startup'
        ]
    },

    zip_safe=False
)