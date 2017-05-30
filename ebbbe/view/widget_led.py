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

from PySide.QtCore import QTimer, Qt
from PySide.QtGui import QWidget, QColor, QPainter, QPen, QBrush, QSizePolicy


class WidgetLed(QWidget):

    def __init__(self, parent, colour='#000000'):
        QWidget.__init__(self, parent)
        self._colour = QColor(colour)

        self.setMinimumSize(20, 20)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self._lit = False
        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self.__flash_off)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        colour = self._colour
        if not self._lit:
            colour = self._colour.darker(300)
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(colour))

        rect = event.rect()
        radius = min(rect.width(), rect.height()) / 3
        painter.drawEllipse(rect.center(), radius, radius)

        painter.end()

    def __flash_off(self):
        self._timer.stop()
        self._lit = False
        self.repaint()

    def flash(self):
        self._lit = True
        self._timer.start()
        self.repaint()

    def light(self, on):
        self._timer.stop()
        self._lit = on
        self.repaint()

    def set_colour(self, colour):
        self._colour = QColor(colour)
