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


class Alu(object):
    def __init__(self, bus, regA, regB):
        self._bus = bus
        self._regA = regA
        self._regB = regB

        self._subtract = False
        self._out = False
        self._carry = False
        self._data = None

        self.reset()

    def reset(self):
        self.clear_flags()
        self._data = 0
        self._carry = False

    def clear_flags(self):
        self._subtract = False
        self._out = False

    def get(self):
        return self._data

    def is_carried(self):
        return self._carry

    def set_subtract(self, enable):
        self._subtract = enable

    def set_out(self, enable):
        self._out = enable

    def clock(self):
        if self._subtract:
            self._data = self._regA.get() - self._regB.get()
            self._carry = self._regB.get() > self._regA.get()
        else:
            self._data = self._regA.get() + self._regB.get()
            self._carry = self._data > 0xff

        self._data &= 0xff

        if self._out:
            self._bus.set(self._data)
