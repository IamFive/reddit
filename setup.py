# -*- coding: utf-8 -*-
#
# @author: Five
# Created on 2013-3-19
#

from setuptools import setup, find_packages
from reddit import version


# read requirements from requirements.txt
with open('requirements.txt') as f:
    requireds = f.read().splitlines()


data_files = []

setup(
      name="reddit",
      version=version(),
      description="Reddit test",
      author="Woo cupid",
      author_email="xmufive@gmail.com",
      license="LGPL",
      data_files=data_files,
      packages=find_packages(),
      install_requires=requireds,
      platforms='any',
      zip_safe=False
)
