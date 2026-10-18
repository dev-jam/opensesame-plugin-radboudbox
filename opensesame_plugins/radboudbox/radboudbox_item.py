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

from libopensesame.base_response_item import BaseResponseItem
from libopensesame.exceptions import OSException
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard

# Interval (ms) for checking whether the background thread has finished
POLL_TIME = 1


class RadboudboxItem(Item):
    """Base class of the Radboud Buttonbox items."""

    def _check_init(self):
        """Checks for the init item and reads its settings."""
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have one instance of `radboudbox_init` at the start of your experiment')
        self.dummy_mode = self.experiment.radboudbox_dummy_mode == 'yes'
        self.verbose = self.experiment.radboudbox_verbose == 'yes'

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)


class RadboudboxResponseItem(RadboudboxItem, BaseResponseItem):
    """Base class of the items that collect a button response. In dummy mode,
    the keyboard is used instead.
    """

    def reset(self):
        self.var.timeout = 'infinite'

    def prepare(self):
        self._check_init()
        super().prepare()
        # rusocsci's waitButtons() fails with a timeout of 0
        if self._timeout == 0:
            raise OSException("Timeout should be more than 0 ms or 'infinite'")

    def prepare_response_func(self):
        if self.dummy_mode:
            self._keyboard = Keyboard(self.experiment,
                                      keylist=self._allowed_responses,
                                      timeout=self._timeout)
            return self._keyboard.get_key

    def process_response(self, response_args):
        response, t1 = response_args
        if not response:
            response = 'NA'
        elif isinstance(response, list):
            response = response[0]
        super().process_response((response, t1))
        response_time = round(t1 - self._t0, 1)
        self._show_message(f"Detected press on button: '{response}'")
        self._show_message(f"Response time: {response_time} ms")

    def _collect_dummy_response(self):
        self._show_message('Dummy mode on, using keyboard')
        self._keyboard.flush()
        super().run()
        self._set_response_time()

    def _wait_until_unlocked(self):
        """Waits until a get buttons start item has its response."""
        while self.experiment.radboudbox_get_buttons_locked:
            self.clock.sleep(POLL_TIME)

    def _wait_buttons(self):
        """Waits for a button and processes the response."""
        if self._timeout is None:
            timeout = float('inf')
        else:
            timeout = self._timeout / 1000
        response = self.experiment.radboudbox.waitButtons(
            maxWait=timeout, buttonList=self._allowed_responses, flush=True)
        t1 = self._set_response_time()
        self.process_response((response, t1))

    def _set_response_time(self, time=None):
        if time is None:
            time = self.clock.time()
        self.experiment.var.set(f'time_response_{self.name}', time)
        return time
