# Filename: setup.py

from setuptools import setup
import io

NAME = ''
VERSION = ''
AUTHOR = ''
AUTHOR_EMAIL = ''
DESCRIPTION = ''
KEYWORDS = ' '.join([])

README = io.open(file='README.rst', mode='r', encoding='utf-8').read()
CHANGES = io.open(file='CHANGES.rst', mode='r', encoding='utf-8').read()
LONG_DESCRIPTION = '\n\n'.join([README, CHANGES])
LICENSE = 'BSD'

URL = ''
DOWNLOAD_URL = ''
CLASSIFIERS = [

]

PACKAGES = []

PACKAGE_DATA = {}

INSTALL_REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    scripts=[]
)