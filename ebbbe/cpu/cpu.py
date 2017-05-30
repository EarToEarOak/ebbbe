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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from ebbbe.cpu.alu import Alu
from ebbbe.cpu.bus import Bus
from ebbbe.cpu.clock import Clock
from ebbbe.cpu.cu import Cu
from ebbbe.cpu.ram import Ram
from ebbbe.cpu.reg import RegProgramCounter, RegMemory, \
    RegInstruct, Register


class Cpu(object):
    def __init__(self):
        self._listener = None

        # Clock
        self._clock = Clock(1, self.__on_clock)

        # Bus
        self._bus = Bus()

        # RAM
        self._ram = Ram(self._bus)

        # Program Counter
        self._pc = RegProgramCounter(self._bus)
        # Memory Address Register
        self._mar = RegMemory(self._bus, self._ram)
        # Instruction Register
        self._ir = RegInstruct(self._bus)
        # A Register
        self._regA = Register(self._bus)
        # B Register
        self._regB = Register(self._bus)
        # Output Register
        self._regOutput = Register(self._bus)

        # Arithmetic and Logic Unit
        self._alu = Alu(self._bus, self._regA, self._regB)

        # Control Unit
        self._cu = Cu(self._clock,
                      self._ram,
                      self._alu,
                      self._pc,
                      self._mar,
                      self._ir,
                      self._regA,
                      self._regB,
                      self._regOutput)

    def __on_clock(self):
        self._cu.on_clock()
        if self._listener is not None:
            self._listener()

    def start(self):
        self._clock.start()

    def stop(self):
        self._clock.stop()

    def set_clock_listener(self, listener):
        self._listener = listener

    def get_periph_clock(self):
        return self._clock

    def get_pc(self):
        return self._pc.get()

    def get_mar(self):
        return self._mar.get()

    def get_ram_dump(self):
        return self._ram.get_dump()

    def get_ram(self):
        return self._ram.get()

    def get_bus(self):
        return self._bus.get()

    def get_ir(self):
        return self._ir.get()

    def get_reg_a(self):
        return self._regA.get()

    def get_reg_b(self):
        return self._regB.get()

    def get_alu(self):
        return self._alu.get()

    def get_cu_seq(self):
        return self._cu.get_seq()

    def get_cu_flags(self):
        return self._cu.get_flags()

    def is_halted(self):
        return self._cu.is_halted()

    def get_reg_out(self):
        return self._regOutput.get()

    def load(self, data):
        self.reset_hard()
        self._ram.set(data)

    def reset_hard(self):
        self.reset_soft()
        self._ram.reset()

    def reset_soft(self):
        self._bus.reset()
        self._cu.reset()
        self._clock.reset()
        self._alu.reset()
        self._pc.reset()
        self._mar.reset()
        self._ir.reset()
        self._regA.reset()
        self._regB.reset()
        self._regOutput.reset()
