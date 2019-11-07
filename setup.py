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
INVENIO_VERSION = "3.1.0"

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.3.3',
    'pydocstyle>=1.0.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

setup_requires = [
    'Babel>=1.3',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'invenio-records-rest>=1.1.0',
    'arrow>=0.12.1',
    'invenio_oauthclient>=1.0.1',
    'invenio[{db},base,auth]~={version}'.format(
        db=DATABASE, version=INVENIO_VERSION),
]

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
    },
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
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
