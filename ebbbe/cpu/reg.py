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


class Register(object):
    def __init__(self, bus):
        self._bus = bus

        self._in = False
        self._out = False
        self._data = None

        self.reset()

    def reset(self):
        self.clear_flags()
        self._data = 0

    def clear_flags(self):
        self._in = False
        self._out = False

    def get(self):
        return self._data

    def set_in(self, enable):
        self._in = enable

    def set_out(self, enable):
        self._out = enable

    def clock(self):
        if self._in:
            self._data = self._bus.get()
        if self._out:
            self._bus.set(self._data)


class RegInstruct(Register):
    def __init__(self, bus):
        Register.__init__(self, bus)

    def clock(self):
        if self._in:
            self._data = self._bus.get()
        if self._out:
            self._bus.set(self._data & 0xf)


class RegMemory(Register):
    def __init__(self, bus, ram):
        Register.__init__(self, bus)
        self._ram = ram

    def clock(self):
        if self._in:
            self._data = self._bus.get() & 0xf
        self._ram.set_address(self._data & 0xf)


class RegProgramCounter(Register):
    def __init__(self, bus):
        Register.__init__(self, bus)
        self._enable = False

        self.reset()

    def reset(self):
        Register.reset(self)
        self.clear_flags()

    def clear_flags(self):
        Register.clear_flags(self)
        self._enable = False

    def set_enable(self, enable):
        self._enable = enable

    def clock(self):
        if self._enable:
            self._data += 1
            self._data &= 0xf
        if self._in:
            self._data = self._bus.get() & 0xf
        if self._out:
            self._bus.set(self._data)
