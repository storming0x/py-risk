#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("./README.md") as readme:
    long_description = readme.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name="pyrisk",
    description="""Cli tools for interacting with Yearn's Risk Framework in Python""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="storm0x.",
    author_email="storm0x@pm.me",
    url="https://github.com/storming0x/py-risk",
    py_modules = ['pyrisk', 'app'],
    packages = find_packages(),
    install_requires = [requirements],
    python_requires='>=3.7',
    keywords="ethereum, yearn",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    entry_points = '''
        [console_scripts]
        pyrisk=pyrisk:cli
    '''
)