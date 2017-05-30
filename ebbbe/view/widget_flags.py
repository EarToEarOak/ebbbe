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

from ebbbe.cpu.cu import Cu
from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led_bank import WidgetLedBank


class WidgetFlags(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.customWidgets = {'WidgetLedBank': WidgetLedBank}

        load_ui(self, 'widget_flags.ui')

        self._widgetLedsControl.set_led_count(len(Cu.FLAG_NAMES), Colour.BLUE,
                                              Cu.FLAG_NAMES, Cu.FLAG_TIPS)

    def set(self, value):
        self._widgetLedsControl.set(value)
