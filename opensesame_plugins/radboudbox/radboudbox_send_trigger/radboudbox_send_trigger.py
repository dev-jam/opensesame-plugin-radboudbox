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

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger


class RadboudboxSendTrigger(Item):

    def reset(self):
        self.var.value = 0
        self.var.pulse_mode = 'no'
        self.var.pulse_time = 50

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        if isinstance(self.var.value, int):
            if self.var.value >= 0 and self.var.value <= 255:
                self.value = int(self.var.value)
            else:
                raise OSException('Trigger value should be between 0 and 255')
        else:
            raise OSException('Trigger value should be a integer')

        if self.pulse_mode == 'yes':
            if isinstance(self.var.pulse_time, int):
                if self.var.pulse_time >= 0:
                    self.pulse_time = int(self.var.pulse_time)
                else:
                    raise OSException('Trigger value should be equal to or larger than 0')
            else:
                raise OSException('Trigger value should be a integer')

        if self.dummy_mode == 'no':
            self.set_item_onset()
            self._show_message(f'Sending trigger value {self.value}')
            self.experiment.radboudbox.sendMarker(val=self.value)
            if self.pulse_mode == 'yes':
                self.clock.sleep(self.pulse_time)
                self.experiment.radboudbox.sendMarker(val=0)

        elif self.dummy_mode == 'yes':
            self._show_message(f'Dummy mode enabled, NOT sending value {self.value}')
        else:
            self._show_message('Error with dummy mode')

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose
        self.extended_mode = self.experiment.radboudbox_extended_mode
        self.pulse_mode = self.var.pulse_mode

    def _check_init(self):
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have one instance of `radboudbox_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtRadboudboxSendTrigger(RadboudboxSendTrigger, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxSendTrigger.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()
        self.line_edit_pulse_time.setEnabled(self.checkbox_pulse_mode.isChecked())
        self.checkbox_pulse_mode.stateChanged.connect(
            self.line_edit_pulse_time.setEnabled)
