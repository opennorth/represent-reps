from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup

setup(
    name='represent-representatives',
    packages=['representatives'],
    version='0.0.1',
    install_requires=[
        'django-appconf',
        'django-jsonfield>=0.7.1',
        'python-dateutil',
    ],
)