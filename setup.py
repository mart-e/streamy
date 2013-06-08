#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import streamy

setup(
    name="streamy",
    version=streamy.__version__,
    packages=find_packages(),
    author="Martin Trigaux",
    author_email="socyallib@dotzero.me",
    description="Python web client to interact with socyal networking websites",
    long_description=open('README.md').read(),
    install_requires=["socyallib", "bottle"],
    include_package_data=True,
    url="https://github.com/mart-e/streamy",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
)
