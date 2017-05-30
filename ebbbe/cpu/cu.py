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


class Cu(object):

    class Flags(object):
        HLT, MI, RI, RO, IO, II, AI, AO, EO, SUB, BI, OI, CE, CO, J = reversed(range(15))

    FLAG_NAMES = ['HLT',
                  'MI',
                  'RI',
                  'RO',
                  'IO',
                  'II',
                  'AI',
                  'AO',
                  'EO',
                  'SUB',
                  'BI',
                  'OI',
                  'CE',
                  'CO',
                  'J'
                  ]

    FLAG_TIPS = ['Halt',
                 'MAR In',
                 'RAM In',
                 'RAM Out',
                 'IR Out',
                 'IR In',
                 'A In',
                 'A Out',
                 'ALU Out',
                 'ALU Subtract',
                 'B In',
                 'O In',
                 'PC Enable',
                 'PC Out',
                 'PC Jump'
                 ]

    _MICROCODE = {
                 # NOP
                 0b0000: [],
                 # LDA
                 0b0001: [[Flags.IO, Flags.MI], [Flags.RO, Flags.AI]],
                 # ADD
                 0b0010: [[Flags.IO, Flags.MI], [Flags.RO, Flags.BI], [Flags.EO, Flags.AI]],
                 # SUB
                 0b0011: [[Flags.IO, Flags.MI], [Flags.RO, Flags.BI], [Flags.EO, Flags.SUB, Flags.AI]],
                 # STA
                 0b0100: [[Flags.IO, Flags.MI], [Flags.AO, Flags.RI]],
                 # JMP
                 0b0110: [[Flags.IO, Flags.J]],
                 # LDI
                 0b0111: [[Flags.IO, Flags.AI]],
                 # JC
                 0b1000: [[]],
                 # OUT
                 0b1110: [[Flags.AO, Flags.OI]],
                 # HLT
                 0b1111: [[Flags.HLT]]
                 }

    def __init__(self,
                 clock,
                 ram,
                 alu,
                 pc,
                 mar,
                 ir,
                 regA,
                 regB,
                 regOutput):

        self._clock = clock
        self._ram = ram
        self._alu = alu
        self._pc = pc
        self._mar = mar
        self._ir = ir
        self._regA = regA
        self._regB = regB
        self._regOutput = regOutput

        self._seq = 0
        self._flags = []

        # Fibonacci Sequence
        self._ram.set([0x71, 0x4e, 0x70, 0xe0, 0x2e, 0x4f, 0x1e, 0x4d,
                       0x1f, 0x4e, 0x1d, 0x80, 0x63, 0x00, 0x00, 0x00])

    def on_clock(self):
        self.__clear_flags()

        # T0: PC to MAR
        if self._seq == 0:
            self._flags = [self.Flags.CO, self.Flags.MI]
            self.__set_flags()
        # T1: RAM to IR
        elif self._seq == 1:
            self._flags = [self.Flags.RO, self.Flags.II, self.Flags.CE]
            self.__set_flags()
        # T2-T4: Execute
        elif self._seq >= 2:
            self.__execute()

        self.__clock()

    def __execute(self):
        opcode = self._ir.get() >> 4
        if opcode in self._MICROCODE:
            microCode = self._MICROCODE[opcode]
            microSeq = self._seq - 2
            if microSeq < len(microCode):
                self._flags = microCode[microSeq]
                self.__set_flags()
            else:
                self.__clear_flags()
        else:
            self.__set_all_flags()

    def __clock(self):
        self._pc.clock()
        self._mar.clock()
        self._ram.clock()
        self._ir.clock()
        self._alu.clock()
        self._regA.clock()
        self._regB.clock()
        self._regOutput.clock()
        self._ram.clock()

        self._seq += 1
        if self._seq > 4:
            self._seq = 0

    def __set_all_flags(self):
        self._flags = list(range(15))
        self.__set_flags()

    def __set_flags(self):
        for flag in self._flags:
            if flag == self.Flags.HLT:
                self._clock.set_hlt(True)
            elif flag == self.Flags.MI:
                self._mar.set_in(True)
            elif flag == self.Flags.RI:
                self._ram.set_in(True)
            elif flag == self.Flags.RO:
                self._ram.set_out(True)
            elif flag == self.Flags.IO:
                self._ir.set_out(True)
            elif flag == self.Flags.II:
                self._ir.set_in(True)
            elif flag == self.Flags.AI:
                self._regA.set_in(True)
            elif flag == self.Flags.AO:
                self._regA.set_out(True)
            elif flag == self.Flags.EO:
                self._alu.set_out(True)
            elif flag == self.Flags.SUB:
                self._alu.set_subtract(True)
            elif flag == self.Flags.BI:
                self._regB.set_in(True)
            elif flag == self.Flags.OI:
                self._regOutput.set_in(True)
            elif flag == self.Flags.CE:
                self._pc.set_enable(True)
            elif flag == self.Flags.CO:
                self._pc.set_out(True)
            elif flag == self.Flags.J:
                self._pc.set_in(True)

    def __clear_flags(self):
        self._flags = []
        self._clock.clear_flags()
        self._ram.clear_flags()
        self._alu.clear_flags()
        self._pc.clear_flags()
        self._mar.clear_flags()
        self._ir.clear_flags()
        self._regA.clear_flags()
        self._regB.clear_flags()
        self._regOutput.clear_flags()

    def reset(self):
        self.__clear_flags()
        self._seq = 0

    def get_seq(self):
        return self._seq

    def get_flags(self):
        data = 0
        for flag in self._flags:
            data |= 1 << flag
        return data

    def is_halted(self):
        return self.Flags.HLT in self._flags
