#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 11:16:14 2019

@author: katsiuba
"""
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()
        
setup(name='myRFMpackage',
      description='What the package does', 
      version='1.0', 
      py_modules=['calculateRFM'],
      install_requires=['pandas','numpy'], 
      packages=['myRFMpackage'])