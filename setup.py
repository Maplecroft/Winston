#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    # Skipping the first line reduces the heading level by 1
    history = ''.join(history_file.readlines()[1:])

requirements = [
    'click==6.6',
    'rasterio==0.36.0',
    'requests[security]==2.4.3',
    'shapely==1.5.17',
    'numpy==1.11.2',
    'tablib==0.11.2',
]

setup(
    name='winston',
    version='0.1.1',
    description="A bit like PostGIS ST_SummaryStats for files on disk",
    long_description=readme + '\n\n' + history,
    author="James Rutherford",
    author_email='james.rutherford@maplecroft.com',
    url='https://github.com/Maplecroft/Winston',
    packages=[
        'winston',
    ],
    package_dir={'winston': 'winston'},
    entry_points={
        'console_scripts': [
            'winston=winston.cli:main'
        ],
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='winston',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
