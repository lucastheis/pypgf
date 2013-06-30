#!/usr/bin/env python

from pgf import __version__
from distutils.core import setup

setup(
	name='pgf',
	version=__version__,
	description='Python interface for PGFPlots',
	author='Lucas Theis',
	author_email='lucas@theis.io',
	url='http://github.com/lucastheis/pypgf',
	license='MIT',
	packages=['pgf'])

