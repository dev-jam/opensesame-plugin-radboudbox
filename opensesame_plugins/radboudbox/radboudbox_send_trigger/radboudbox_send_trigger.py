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

from libopensesame.exceptions import OSException
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from ..radboudbox_item import RadboudboxItem


class RadboudboxSendTrigger(RadboudboxItem):

    def reset(self):
        self.var.value = 0
        self.var.pulse_mode = 'no'
        self.var.pulse_time = 50

    def prepare(self):
        super().prepare()
        self._check_init()
        self.pulse_mode = self.var.pulse_mode == 'yes'

    def run(self):
        # The value and pulse time may be set by an earlier item
        value = self.var.value
        if not isinstance(value, int):
            raise OSException('Trigger value should be an integer')
        if not 0 <= value <= 255:
            raise OSException('Trigger value should be between 0 and 255')
        self.value = value

        if self.pulse_mode:
            pulse_time = self.var.pulse_time
            if not isinstance(pulse_time, int):
                raise OSException('Pulse time should be an integer')
            if pulse_time < 0:
                raise OSException('Pulse time should be equal to or larger than 0')
            self.pulse_time = pulse_time

        # Nothing between sending and resetting the trigger, so the messages
        # come last. Dummy mode waits as well, so the timing is the same.
        if not self.dummy_mode:
            self.experiment.radboudbox.sendMarker(val=self.value)
        self.set_item_onset()
        if self.pulse_mode:
            self.clock.sleep(self.pulse_time)
            if not self.dummy_mode:
                self.experiment.radboudbox.sendMarker(val=0)
        pulse = f', pulse of {self.pulse_time} ms' if self.pulse_mode else ''
        if self.dummy_mode:
            self._show_message(f'Dummy mode enabled, NOT sending value {self.value}{pulse}')
        else:
            self._show_message(f'Sent trigger value {self.value}{pulse}')


class QtRadboudboxSendTrigger(RadboudboxSendTrigger, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxSendTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.line_edit_pulse_time.setEnabled(self.checkbox_pulse_mode.isChecked())
        self.checkbox_pulse_mode.stateChanged.connect(
            self.line_edit_pulse_time.setEnabled)
