# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 CESNET.
#
# Invenio OpenID Connect is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio OpenID Connect Auth Backend"""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()

DATABASE = "postgresql"
OAREPO_VERSION = os.environ.get('OAREPO_VERSION', '3.1.1')

tests_require = [
]

setup_requires = [
    'pytest-runner>=3.0.0,<5',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'arrow>=0.12.1',
    'invenio-db>=1.0.0',
    'invenio_oauthclient>=1.0.1',
]

extras_require = {
    'tests': [
        'oarepo[tests]~={version}'.format(
            version=OAREPO_VERSION),
        'pydocstyle>=5'
    ],
    'tests-es7': [
        'oarepo[tests-es7]~={version}'.format(
            version=OAREPO_VERSION),
        'pydocstyle>=5'
    ],
}

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_openid_connect', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-openid-connect',
    version=version,
    description=__doc__,
    long_description=readme,
    keywords='invenio-openid-connect Invenio',
    license='MIT',
    author='Miroslav Bauer',
    author_email='bauer@cesnet.cz',
    url='https://github.com/oarepo/invenio-openid-connect',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_openid_connect = invenio_openid_connect:InvenioOpenIDConnect',
        ],
        'invenio_base.api_apps': [
            'invenio_openid_connect = invenio_openid_connect:InvenioOpenIDConnect',
        ],
        'invenio_base.api_blueprints': [
            'invenio_openid_connect = invenio_openid_connect.views:blueprint',
        ],
    },
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
    ],
)
