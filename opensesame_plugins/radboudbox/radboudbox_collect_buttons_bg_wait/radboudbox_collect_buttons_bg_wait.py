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

from libopensesame.exceptions import OSException
from ..radboudbox_item import RadboudboxItem


class RadboudboxCollectButtonsBgWait(RadboudboxItem):

    def prepare(self):
        super().prepare()
        self._check_init()
        # The shared state keeps the names it had before 6.0.0 (get buttons
        # start and wait): inline scripts may use them
        self.experiment.radboudbox_get_buttons_wait = True

    def run(self):
        self._check_start()
        self.set_item_onset()
        # In dummy mode, the start item has collected the response already
        if not self.dummy_mode:
            self.experiment.radboudbox_get_buttons_thread.join()
            self.experiment.radboudbox_get_buttons_thread_running = 0
        self.experiment.radboudbox_get_buttons = False
        error = getattr(self.experiment, 'radboudbox_get_buttons_error', None)
        if error is not None:
            self.experiment.radboudbox_get_buttons_error = None
            raise OSException(f'Collecting buttons in the background failed: '
                              f'{error}') from error

    def _check_start(self):
        if not hasattr(self.experiment, "radboudbox_get_buttons_start"):
            raise OSException('`radboudbox_collect_buttons_bg_start` item is missing')
        if not self.experiment.radboudbox_get_buttons:
            raise OSException('Radboudbox not waiting for a button, you first '
                              'have to start the buttonbox before waiting')
