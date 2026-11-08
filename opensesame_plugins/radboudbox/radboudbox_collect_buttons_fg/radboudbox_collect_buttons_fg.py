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

from ..radboudbox_item import RadboudboxResponseItem


class RadboudboxCollectButtonsFg(RadboudboxResponseItem):

    def run(self):
        self._t0 = self.set_item_onset()
        if self.dummy_mode:
            self._collect_dummy_response()
            return
        self._wait_until_unlocked()
        self._show_message('Start collecting buttons')
        self._wait_buttons()
