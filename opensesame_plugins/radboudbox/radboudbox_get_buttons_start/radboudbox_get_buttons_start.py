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

import threading

from libopensesame.exceptions import OSException
from ..radboudbox_item import RadboudboxResponseItem


class RadboudboxGetButtonsStart(RadboudboxResponseItem):

    def prepare(self):
        super().prepare()
        self.experiment.radboudbox_get_buttons_start = True

    def run(self):
        self._check_wait()
        self._t0 = self.set_item_onset()
        if self.dummy_mode:
            # The keyboard can't be read in a thread: collect the response now
            self.experiment.radboudbox_get_buttons = True
            self._collect_dummy_response()
            return
        self._wait_until_unlocked()
        self._show_message('Start collecting buttons')
        started = threading.Event()
        thread = threading.Thread(target=self._wait_buttons_in_background,
                                  args=(started,))
        self.experiment.radboudbox_get_buttons_thread = thread
        self.experiment.radboudbox_get_buttons_error = None
        self.experiment.radboudbox_get_buttons_locked = 1
        self.experiment.radboudbox_get_buttons = True
        thread.start()
        started.wait()
        # Compensates for the initialization of the buttonbox
        self.clock.sleep(1)

    def _wait_buttons_in_background(self, started):
        self.experiment.radboudbox_get_buttons_thread_running = 1
        started.set()
        try:
            self._wait_buttons()
        except Exception as e:
            # Raised by the wait item
            self.experiment.radboudbox_get_buttons_error = e
        finally:
            self.experiment.radboudbox_get_buttons_locked = 0

    def _check_wait(self):
        if not hasattr(self.experiment, "radboudbox_get_buttons_wait"):
            raise OSException('`Radboudbox Get Buttons Wait` item is missing')
        if self.experiment.radboudbox_get_buttons:
            raise OSException('Radboudbox already waiting for a button, you '
                              'first have to stop the buttonbox before '
                              'starting')
