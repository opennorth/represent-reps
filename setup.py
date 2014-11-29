from setuptools import setup

setup(
    name="represent-representatives",
    version="0.2",
    description="A web API for elected officials tied to electoral districts, packaged as a Django app.",
    url="https://github.com/rhymeswithcycle/represent-reps",
    license="MIT",
    packages=[
        'representatives',
        'representatives.management',
        'representatives.management.commands',
    ],
    install_requires=[
        'django-appconf',
        'django-jsonfield>=0.7.1',
        'represent-boundaries',
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ],
)
