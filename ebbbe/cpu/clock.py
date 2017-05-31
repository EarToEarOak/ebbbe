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

import threading


class Clock(object):
    def __init__(self, frequency, callback):
        self._callback = callback
        self._eventStop = threading.Event()
        self._threadClock = Clock.ClockThread(frequency, self._eventStop, callback)

    def start(self):
        if self._threadClock is not None:
            self._threadClock.start()

    def stop(self):
        if self._threadClock is not None:
            self._eventStop.set()

    def get_frequency(self):
        return self._threadClock.get_frequency()

    def set_frequency(self, frequency):
        self._threadClock.set_frequency(frequency)

    def set_hlt(self, enable):
        self._threadClock.set_hlt(enable)

    def set_run(self, enable):
        self._threadClock.set_run(enable)

    def step(self):
        self._threadClock.step()

    def reset(self):
        self.clear_flags()

    def clear_flags(self):
        self.set_hlt(False)

    class ClockThread(threading.Thread):
        def __init__(self, frequency, event, callback):
            threading.Thread.__init__(self)
            self._frequency = frequency
            self._event = event
            self._callback = callback

            self._halt = False
            self._run = False

        def run(self):
            while not self._event.wait(1. / self._frequency):
                if self._run:
                    self.step()

        def step(self):
            if not self._halt:
                self._callback()

        def get_frequency(self):
            return self._frequency

        def set_frequency(self, frequency):
            self._frequency = frequency
            self._event.set()
            self._event.clear()

        def set_hlt(self, enable):
            self._halt = enable

        def set_run(self, enable):
            self._run = enable
