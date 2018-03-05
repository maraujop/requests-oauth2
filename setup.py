#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.3.0'

with open('README.md') as f:
    long_description = f.read()


setup(
    name='requests-oauth2',
    version=version,
    description='OAuth2 support to Python-Requests HTTP library.',
    long_description=long_description,
    author='Miguel Araujo',
    author_email='miguel.araujo.perez@gmail.com',
    url='http://github.com/maraujop/requests-oauth2',
    packages=find_packages(),
    install_requires=['requests', 'six'],
    license='BSD',
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ),
    keywords=['requests', 'python-requests', 'OAuth', 'OAuth2'],
    zip_safe=False,
)
