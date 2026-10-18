"""
This file is part of OpenSesame.

OpenSesame is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

OpenSesame is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with OpenSesame.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

from ..radboudbox_item import RadboudboxResponseItem


class RadboudboxWaitButtons(RadboudboxResponseItem):

    def run(self):
        self._t0 = self.set_item_onset()
        if self.dummy_mode:
            self._collect_dummy_response()
            return
        self._wait_until_unlocked()
        self._show_message('Start collecting buttons')
        self._wait_buttons()
