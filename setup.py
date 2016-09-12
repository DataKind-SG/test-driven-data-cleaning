from setuptools import setup
import os


version_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'VERSION')
version = open(version_file, 'rt').read().strip()

install_requires = [
    'backports.functools_lru_cache==1.2.1',
    'docopt==0.6.2',
    'py-trello==0.4.3',
    'PyYAML==3.11',
]

setup(
    name='test-driven-data-cleaning',
    install_requires=install_requires,
    version=version,
    packages=['tddc'],
    package_data={'': ['VERSION', '*.sql']},
    url='https://github.com/DataKind-SG/test-driven-data-cleaning',
    author='Oliver Chen',
    author_email='oliverxchen@gmail.com'
)
