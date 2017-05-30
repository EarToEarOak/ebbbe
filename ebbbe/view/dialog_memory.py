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

from PySide.QtCore import Signal
from PySide.QtGui import QDialog, QFont

from ebbbe.view.ui import load_ui
from ebbbe.view.utils import win_remove_context_help


class DialogMemory(QDialog):
    _REF, _VAL, _NUL = range(3)

    _OPCODES = {
          0b0000: ['nop', _NUL],
          0b0001: ['lda', _REF],
          0b0010: ['add', _REF],
          0b0011: ['sub', _REF],
          0b0100: ['sta', _REF],
          0b0110: ['jmp', _VAL],
          0b0111: ['ldi', _VAL],
          0b1000: ['jc', _VAL],
          0b1110: ['out', _NUL],
          0b1111: ['hlt', _NUL]
         }

    closed = Signal()

    def __init__(self, cpu):
        QDialog.__init__(self)

        self._cpu = cpu

        load_ui(self, 'dialog_memory.ui')

        win_remove_context_help(self)

        self.update()
        self.adjustSize()

        font = QFont('Monospace')
        font.setStyleHint(QFont.TypeWriter)
        font.setPointSize(12)
        self._textMem.setFont(font)

    def closeEvent(self, _event):
        self.closed.emit()

    def update(self):
        references = []
        address = 0

        display = 'Address\tContents\t\tPC\tMAR\n\n'
        for location in self._cpu.get_ram_dump():
            operand = ''
            if address in references:
                opcode = ['0x{:02x}'.format(location), None]
            else:
                if location >> 4 in self._OPCODES:
                    opcode = self._OPCODES[location >> 4]
                    if opcode[1] == self._REF:
                        operand = '[0x{:1x}]'.format(location & 0xf)
                        references.append(location & 0xf)
                    elif opcode[1] == self._VAL:
                        operand = '0x{:1x} '.format(location & 0xf)
                else:
                    opcode = ['?', None]

            pc = ''
            if address == self._cpu.get_pc():
                pc = '<'
            mar = ''
            if address == self._cpu.get_mar():
                mar = '<'

            display += '0x{:01x}: \t0x{:02x}   {:4s} {:4s} \t{:1s} \t{:1s}\n'.format(address,
                                                                                     location,
                                                                                     opcode[0],
                                                                                     operand,
                                                                                     pc, mar)
            address += 1

        self._textMem.setText(display)
