#!/usr/bin/env python3

# see http://bugs.python.org/issue8876
# this is just a quick hack so we can test build in vagrant
import os
if os.environ.get('USER','') == 'vagrant':
  del os.link

from setuptools import setup, find_packages

setup(name='openregister-conformance',
      version='0.1.0',
      description='Openregister conformance tests',
      long_description='Tests to search for openregister specification conformance issues',
      author='Openregister.org',
      author_email='philip.potter@digital.cabinet-office.gov.uk',
      url='https://github.com/openregister/conformance-test',
      download_url='https://github.com/openregister/conformance-test',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      license='MIT',
      platforms='any',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python :: 3.4',
        ],
      scripts=['openregister-conformance'],
      setup_requires=[
        'pytest-runner'
      ],
      tests_require=['pytest>=2.9.0'],
      install_requires=[
        'pytest>=2.9.0',
        'requests>=2.9.1'
      ]
)
