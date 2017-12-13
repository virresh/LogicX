"""
LogicX app for running flask apps on Bluemix
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LogicX',
    version='1.0.0',
    description='App to teach students the basics of Programming',
    long_description=long_description,
    url='https://github.com/virresh/LogicX',
    license='GPL-3.0'
)
