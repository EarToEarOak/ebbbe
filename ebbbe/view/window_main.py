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

import os
import struct
import time

from PySide.QtCore import Signal, Qt, Slot
from PySide.QtGui import QMainWindow, QFileDialog, QMessageBox
from ebbbe.view.dialog_about import DialogAbout
from ebbbe.view.dialog_memory import DialogMemory
from ebbbe.view.settings import Settings
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_bus import WidgetBus
from ebbbe.view.widget_clock import WidgetClock
from ebbbe.view.widget_flags import WidgetFlags
from ebbbe.view.widget_ir import WidgetIr
from ebbbe.view.widget_mar import WidgetMar
from ebbbe.view.widget_out import WidgetOut
from ebbbe.view.widget_pc import WidgetPc
from ebbbe.view.widget_reg import WidgetReg
from ebbbe.view.widget_seq import WidgetSeq

from ebbbe.view.widget_ram import WidgetRam


class WindowMain(QMainWindow):

    signalUpdate = Signal()

    def __init__(self, cpu):
        QMainWindow.__init__(self)

        self._cpu = cpu
        self._lastUpdate = 0
        self._dialogMem = None

        self._settings = Settings()

        self.customWidgets = {'WidgetClock': WidgetClock,
                              'WidgetPc': WidgetPc,
                              'WidgetMar': WidgetMar,
                              'WidgetIr': WidgetIr,
                              'WidgetBus': WidgetBus,
                              'WidgetReg': WidgetReg,
                              'WidgetSeq': WidgetSeq,
                              'WidgetFlags': WidgetFlags,
                              'WidgetOut': WidgetOut,
                              'WidgetRam': WidgetRam}

        load_ui(self, 'window_main.ui')

        self._widgetRegA.set_label('A', Qt.AlignRight)
        self._widgetRegA.set_tooltip('A Register (Accumulator)')
        self._widgetAlu.set_label('ALU', Qt.AlignRight)
        self._widgetAlu.set_tooltip('Arithmetic and Logic Unit')
        self._widgetRegB.set_label('B', Qt.AlignRight)
        self._widgetRegB.set_tooltip('B Register')

        self._widgetClock.set_periph(cpu.get_periph_clock())
        self._widgetClock.set_frequency(self._settings.frequency)

        self.adjustSize()

        self.signalUpdate.connect(self.__update)
        cpu.set_clock_listener(self.signalUpdate.emit)

        self._widgetRam.signalWrite.connect(self.__set_ram_value)
        self._widgetMar.signalSet.connect(self.__set_mar_value)

        self.__update(False)

    def closeEvent(self, _event):
        if self._dialogMem:
            self._dialogMem.close()
        self._cpu.stop()

        self._settings.frequency = self._widgetClock.get_frequency()
        self._settings.save()

    @Slot()
    def on_actionOpen_triggered(self):
        filename, _ = QFileDialog.getOpenFileName(self,
                                                  dir=self._settings.dirFile,
                                                  filter='Binary files (*.bin);;All files (*.*)')
        if filename:
            self._settings.dirFile, _ = os.path.split(filename)
            self.__open(filename)

    @Slot()
    def on_actionExit_triggered(self):
        self.close()

    @Slot(bool)
    def on_actionMemory_triggered(self, checked):
        if checked and self._dialogMem is None:
            self._dialogMem = DialogMemory(self._cpu)
            self._dialogMem.show()
            self._dialogMem.closed.connect(self.__on_mem_closed)
        elif self._dialogMem is not None:
            self._dialogMem.close()

    @Slot()
    def on_actionAbout_triggered(self):
        dlg = DialogAbout()
        dlg.exec_()

    @Slot()
    def on_actionResetSoft_triggered(self):
        self._cpu.reset_soft()
        self._widgetMar.reset()
        self.__update(flash=False, force=True)

    @Slot()
    def on_actionResetHard_triggered(self):
        self._cpu.reset_hard()
        self._widgetMar.reset()
        self.__update(flash=False, force=True)

    def __on_mem_closed(self):
        self._dialogMem = None
        self.actionMemory.setChecked(False)

    def __update(self, flash=True, force=False):
        cpu = self._cpu
        if time.time() - self._lastUpdate > 0.016 or cpu.is_halted() or force:
            if flash:
                self._widgetClock.flash()
            self._widgetPc.set(cpu.get_pc())
            self._widgetMar.set(cpu.get_mar())
            self._widgetBus.set(cpu.get_bus())
            self._widgetRam.set(cpu.get_ram())
            self._widgetIr.set(cpu.get_ir())
            self._widgetRegA.set(cpu.get_reg_a())
            self._widgetRegB.set(cpu.get_reg_b())
            self._widgetAlu.set(cpu.get_alu())
            self._widgetSeq.set(cpu.get_cu_seq())
            self._widgetFlags.set(cpu.get_cu_flags())
            self._widgetOut.set(cpu.get_reg_out())
            if self._dialogMem is not None:
                self._dialogMem.update()
            self._lastUpdate = time.time()

    def __open(self, filename):
        try:
            with open(filename, 'rb') as f:
                data = struct.unpack('B' * 16, f.read())
                self._cpu.load(list(data))
                self.__update(False)
        except struct.error:
            QMessageBox.critical(self, 'Error', "Files should be 16 bytes in size")

    def __set_ram_value(self, value):
        self._cpu.set_ram_value(value)
        self.__update(flash=False, force=True)

    def __set_mar_value(self, setter, value):
        self._widgetClock.enable(not setter)
        self._cpu.set_mar(value)
        self.__update(flash=False, force=True)

