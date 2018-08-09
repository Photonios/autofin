import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as readme:
    README = readme.read().split('h1>\n\n', 2)[1]

setup(
    name='autofin',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='Bringing all of PostgreSQL\'s awesomeness to Django.',
    description='Automatically track finance related things.',
    long_description=README,
    url='https://github.com/Photonios/autofin',
    author='Swen Kooij',
    author_email='swenkooij@gmail.com',
    keywords=['autofin', 'swen', 'kooij', 'finance', 'track'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
