from setuptools import setup
import os
import re


try:
    version_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'VERSION')
    version = open(version_file, 'rt').read().strip()
except IOError:
    package_info_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'PKG-INFO')
    info = open(package_info_file, 'rt').read()
    version = re.search('\nVersion: (.*)\n', info).group(1)

install_requires = [
    'backports.functools_lru_cache==1.2.1',
    'docopt==0.6.2',
    'py-trello==0.6.1',
    'PyYAML==3.12',
]

short_description = 'Scaffold out methods and tests for collaborative data ' \
                    'cleaning.'

long_description = 'This package provides a framework for collaborative, ' \
                   'test-driven data cleaning. The framework enables a ' \
                   'reproducible method for data cleaning that can be easily ' \
                   'validated. \n\nFor a given tabular data set, a Trello ' \
                   'board is populated with cards for each column so that ' \
                   'team members can tag themselves to a column and ensure ' \
                   'that work does not overlap. The cards include summary ' \
                   'statistics of the columns that can be useful for writing ' \
                   'methods to clean the column. Method stubs and test ' \
                   'stubs are also scaffolded out for team members to fill ' \
                   'out.'

setup(
    name='tddc',
    install_requires=install_requires,
    version=version,
    packages=['tddc'],
    scripts=['bin/tddc'],
    url='https://github.com/DataKind-SG/test-driven-data-cleaning',
    author='Oliver Chen',
    author_email='oliverxchen@gmail.com',
    description=short_description,
    long_description=long_description,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='data cleaning collaborative'
)
