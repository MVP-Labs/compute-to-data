#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""

#  Copyright 2020 Ownership Labs
#  SPDX-License-Identifier: Apache-2.0

import os
from os.path import join

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

# Installed by pip install ocean-lib
# or pip install -e .
install_requirements = [
    "coloredlogs==15.0",
    "Flask==1.1.2",
    "Flask-Cors==3.0.9",
    "psycopg2-binary",
    "requests==2.25.1",
    "demjson==2.2.4",
]

# Required to run setup.py:
setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest',
]

# Possibly required by developers of ownership-worker:
dev_requirements = [
    'pytest',
]

docs_requirements = [
    'Sphinx',
    'sphinxcontrib-apidoc',
]

packages = []
for d, _, _ in os.walk('worker'):
    if os.path.exists(join(d, '__init__.py')):
        packages.append(d.replace(os.path.sep, '.'))

setup(
    author="iwzy7071",
    author_email='iwzy7071@aliyun.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
    ],
    description="worker",
    extras_require={
        'test': test_requirements,
        'dev': dev_requirements + test_requirements + docs_requirements,
        'docs': docs_requirements,
    },
    install_requires=install_requirements,
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='ownership-worker',
    name='ownership-worker',
    packages=packages,
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ownership-labs/worker',
    version='0.0.5',
    zip_safe=False,
)
