from setuptools import setup

setup(
    name="represent-representatives",
    version="0.3",
    description="A web API for elected officials tied to electoral districts, packaged as a Django app.",
    url="https://github.com/opennorth/represent-reps",
    license="MIT",
    packages=[
        'representatives',
        'representatives.management',
        'representatives.management.commands',
        'representatives.migrations',
    ],
    install_requires=[
        'django-appconf',
        'represent-boundaries',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ],
)
