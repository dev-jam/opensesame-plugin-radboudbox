"""
This file is part of opensesame-plugin-radboudbox.

Copyright (C) 2016-2026 Bob Rosbag <mail@bobrosbag.nl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

__author__ = "Bob Rosbag"
__license__ = "GPL-3.0-or-later"

import threading

from libopensesame.exceptions import OSException
from ..radboudbox_item import RadboudboxResponseItem


class RadboudboxCollectButtonsBgStart(RadboudboxResponseItem):

    background = True

    def prepare(self):
        super().prepare()
        # The shared state keeps the names it had before 6.0.0 (get buttons
        # start and wait): inline scripts may use them
        self.experiment.radboudbox_get_buttons_start = True

    def run(self):
        self._check_wait()
        self._t0 = self.set_item_onset()
        # Collects without end: only a bg stop item ends it
        infinite = self._number_of_responses is None and self._timeout is None
        if self.dummy_mode:
            # The keyboard can't be read in a thread: collect the response now
            self.experiment.radboudbox_get_buttons = True
            self.experiment.radboudbox_get_buttons_infinite = int(infinite)
            if infinite:
                # Nothing could end it here: one key, as with 1 response
                self._show_message('Dummy mode: number of responses and '
                                   'timeout infinite, collecting one key')
                self._number_of_responses = 1
            self._collect_dummy_response()
            return
        self._wait_until_unlocked()
        self.experiment.radboudbox_get_buttons_infinite = int(infinite)
        self._show_message('Start collecting buttons')
        started = threading.Event()
        stop_event = threading.Event()
        thread = threading.Thread(target=self._wait_buttons_in_background,
                                  args=(started, stop_event))
        self.experiment.radboudbox_get_buttons_stop_event = stop_event
        self.experiment.radboudbox_get_buttons_thread = thread
        self.experiment.radboudbox_get_buttons_error = None
        self.experiment.radboudbox_get_buttons_locked = 1
        self.experiment.radboudbox_get_buttons = True
        thread.start()
        started.wait()
        # Compensates for the initialization of the buttonbox
        self.clock.sleep(1)

    def _wait_buttons_in_background(self, started, stop_event):
        self.experiment.radboudbox_get_buttons_thread_running = 1
        started.set()
        try:
            self._wait_buttons(stop_event)
        except Exception as e:
            # Raised by the wait or stop item
            self.experiment.radboudbox_get_buttons_error = e
        finally:
            self.experiment.radboudbox_get_buttons_locked = 0

    def _check_wait(self):
        if not hasattr(self.experiment, "radboudbox_get_buttons_wait") and \
                not hasattr(self.experiment, "radboudbox_get_buttons_stop"):
            raise OSException('`radboudbox_collect_buttons_bg_wait` or '
                              '`radboudbox_collect_buttons_bg_stop` item is '
                              'missing')
        if self.experiment.radboudbox_get_buttons:
            raise OSException('Radboudbox already waiting for a button, you '
                              'first have to stop the buttonbox before '
                              'starting')
