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
        'representatives.migrations',
    ],
    install_requires=[
        'django-appconf',
        # @see https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#jsonfield Django 1.9 and PostgreSQL 9.4
        'jsonfield>=0.9.20,<1',
        'represent-boundaries',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
    ],
)
