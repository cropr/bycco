import os

from setuptools import setup, find_packages

requires = []

setup(
    name='bycco',
    version='0.7.3',
    description='BYC 2019',
    long_description='Belgian Youth Chess Cheampionships 2019',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Django-cms",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Ruben Decrop',
    author_email='ruben@decrop.net',
    url='https://www.bycco.be',
    keywords='chess, youth, chempionships Belgium, 2018',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
