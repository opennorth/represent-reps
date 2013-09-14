from setuptools import setup

setup(
    name='represent-representatives',
    description='A Web API for political representatives tied to geographical districts. Packaged as a Django app.',
    url='https://github.com/rhymeswithcycle/represent-reps',
    packages=['representatives', 'representatives.management', 'representatives.management.commands'],
    version='0.1',
    install_requires=[
        'django-appconf',
        'django-jsonfield>=0.7.1',
        'python-dateutil',
        'represent-boundaries',
    ],
    classifiers = [
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ]
)