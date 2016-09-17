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
