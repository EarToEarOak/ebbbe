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

from PySide.QtGui import QWidget

from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led_bank import WidgetLedBank


class WidgetSeq(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.customWidgets = {'WidgetLedBank': WidgetLedBank}

        load_ui(self, 'widget_seq.ui')

        self._widgetLedSeq.set_led_count(3, Colour.RED, reverse=True)
        names = ['T0', 'T1', 'T2', 'T3', 'T4']
        self._widgetLedStep.set_led_count(5, Colour.GREEN, names, toolTip=False)

    def set(self, value):
        self._widgetLedSeq.set(value)
        leds = 0b111101111 >> value
        self._widgetLedStep.set(leds)
