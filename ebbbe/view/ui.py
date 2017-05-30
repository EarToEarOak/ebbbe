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


from PySide.QtCore import QMetaObject
from PySide.QtUiTools import QUiLoader

from ebbbe.view.utils import get_resource


class UiLoader(QUiLoader):
    def __init__(self, instance):
        QUiLoader.__init__(self, instance)
        self._instance = instance

    def createWidget(self, className, parent=None, name=''):
        widget = None
        if parent is None and self._instance:
            widget = self._instance
        elif className in QUiLoader.availableWidgets(self):
            widget = QUiLoader.createWidget(self,
                                            className,
                                            parent,
                                            name)
        else:
            if hasattr(self._instance, 'customWidgets'):
                if className in self._instance.customWidgets.keys():
                    widget = self._instance.customWidgets[className](parent)
                else:
                    error = 'Unknown widget \'{}\''.format(className)
                    raise KeyError(error)
            else:
                error = 'Instance does not specify \'customWidgets\''
                raise AttributeError(error)

        if self._instance is not None and widget is not None:
            setattr(self._instance, name, widget)

        return widget


def load_ui(instance, fileName):
    loader = UiLoader(instance)
    uiFile = get_resource(fileName)
    widget = loader.load(uiFile)
    QMetaObject.connectSlotsByName(widget)

    return widget
