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


class Ram(object):
    def __init__(self, bus):
        self._bus = bus

        self._in = False
        self._out = False
        self._address = None
        self._data = None

        self.reset()

    def reset(self):
        self._address = 0
        self._data = [0] * 16

    def clear_flags(self):
        self._in = False
        self._out = False

    def get_dump(self):
        return self._data

    def get(self):
        return self._data[self._address]

    def set(self, data):
        self._data = data

    def set_value(self, value):
        self._data[self._address] = value

    def set_in(self, load):
        self._in = load

    def set_out(self, enable):
        self._out = enable

    def set_address(self, address):
        self._address = address

    def clock(self):
        if self._in:
            self._data[self._address] = self._bus.get()
        if self._out:
            self._bus.set(self._data[self._address])
