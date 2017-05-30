#!/usr/bin/env python
#
#
# 8-Bit Breadboard Emulator
#
# https://eartoearoak.com/ebbbe
#
# Copyright 2017 Al Brown
#
# An emulation of of Ben Eater's 8-bit breadboard computer (https://eater.net/8bit/)
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from setuptools import setup, find_packages

from ebbbe.version import VERSION

setup(name='ebbbe',
      version='.'.join([str(x) for x in VERSION]),
      description='An emulation of of Ben Eater\'s 8-bit breadboard computer (https://eater.net/8bit/)',
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Education',
                   'Topic :: System :: Emulators'],
      keywords='8-bit breadboard computer emulator',
      url='https://eartoearoak.com/software/ebbbe',
      author='Al Brown',
      author_email='al [at] eartoearok.com',
      license='GPLv2',
      packages=find_packages(),
      package_data={'ebbbe.view.res': ['*']},
      scripts=['ebbbe_start.py'],
      install_requires=['PySide'])
