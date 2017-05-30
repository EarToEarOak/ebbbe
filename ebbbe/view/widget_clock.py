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

from PySide.QtCore import Slot
from PySide.QtGui import QWidget

from ebbbe.view.constants import Colour
from ebbbe.view.ui import load_ui
from ebbbe.view.widget_led import WidgetLed


class WidgetClock(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.customWidgets = {'WidgetLed': WidgetLed}

        load_ui(self, 'widget_clock.ui')

        self._periph = None

        self._ledClock.set_colour(Colour.BLUE)

    @Slot(int)
    def on__dialFreq_valueChanged(self, value):
        self._periph.set_frequency(value / 4.)
        self.__update()

    @Slot(bool)
    def on__buttonStep_clicked(self, _checked):
        self._buttonRun.setChecked(False)
        self._periph.set_run(True)
        self._periph.step()

    @Slot(bool)
    def on__buttonRun_clicked(self, checked):
        self._periph.set_run(not checked)

    def __update(self):
        freq = self._dialFreq.value()
        self._labelFreq.setText('{} Hz'.format(freq / 4.))

    def set_periph(self, periph):
        self._periph = periph
        self._dialFreq.setValue(periph.get_frequency() * 4)
        self.__update()

    def set_frequency(self, frequency):
        self._periph.set_frequency(frequency)
        self._dialFreq.setValue(frequency * 4)

    def get_frequency(self):
        return self._periph.get_frequency()

    def flash(self):
        self._ledClock.flash()
