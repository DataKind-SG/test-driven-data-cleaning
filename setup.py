from setuptools import setup
import os
import re


try:
    version_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'VERSION')
    version = open(version_file, 'rt').read().strip()
except FileNotFoundError:
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

setup(
    name='tddc',
    install_requires=install_requires,
    version=version,
    packages=['tddc'],
    url='https://github.com/DataKind-SG/test-driven-data-cleaning',
    author='Oliver Chen',
    author_email='oliverxchen@gmail.com'
)
