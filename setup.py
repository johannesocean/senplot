# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-03-11 13:47
@author: johannes
"""
import os
import setuptools


requirements = []
with open('requirements.txt', 'r') as fh:
    for line in fh:
        requirements.append(line.strip())

NAME = 'senplot'
README = open('READMEpypi.rst', 'r').read()

setuptools.setup(
    name=NAME,
    version="0.0.1",
    author="SMHI - NODC",
    author_email="johannes.johansson@smhi.se",
    description="Example plotting of Sentinel 3 data at the Swedish NODC",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JohannesSMHI/senplot",
    packages=setuptools.find_packages(),
    package_data={'senplot': [
        os.path.join('etc', '*.xlsx'),
        os.path.join('etc', 'readers', '*.yaml'),
        os.path.join('etc', 'validators', '*.yaml'),
        os.path.join('etc', 'writers', '*.yaml'),
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)
