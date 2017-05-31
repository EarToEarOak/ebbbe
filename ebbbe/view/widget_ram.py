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

from PySide.QtCore import Qt, Slot, Signal
from PySide.QtGui import QWidget
from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led_bank import WidgetLedBank

from ebbbe.view.widget_dip import WidgetDip


class WidgetRam(QWidget):
    signalWrite = Signal(int)

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.customWidgets = {'WidgetLedBank': WidgetLedBank,
                              'WidgetDip': WidgetDip}

        load_ui(self, 'widget_ram.ui')

        self._widgetLeds.set_led_count(8, Colour.RED)
        self._widgetDip.set_dip_count(8)

    @Slot(bool)
    def on__buttonWrite_clicked(self, _checked):
        value = self._widgetDip.get()
        self.signalWrite.emit(value)

    def set_label(self, label, align=Qt.AlignLeft):
        self._label.setText(label)
        self._label.setAlignment(align)

    def set_tooltip(self, tip):
        self.setToolTip(tip)

    def set(self, value):
        self._widgetLeds.set(value)
