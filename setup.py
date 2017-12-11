import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = []

setup(
    name='bycco',
    version='0.3.0',
    description='Belgian Youtth Chess Championshops 2018',
    long_description=README + '\n\n' + CHANGES,
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
