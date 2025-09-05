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

CMD_DICT = {'Calibrate Sound': ['C', 'S'],
            'Calibrate Voice': ['C', 'V'],
            'Detect Sound': ['D', 'S'],
            'Detect Voice': ['D', 'V'],
            'Marker Out': ['M'],
            'Pulse Out': ['P'],
            'Pulse Time': ['X'],
            'Analog Out 1': ['Y'],
            'Analog Out 2': ['Z'],
            'Tone': ['T'],
            'Analog In 1': ['A', '1'],
            'Analog In 2': ['A', '2'],
            'Analog In 3': ['A', '3'],
            'Analog In 4': ['A', '4'],
            'LEDs Off': ['L', 'X'],
            'LEDs Input': ['L', 'I'],
            'LEDs Output': ['L', 'O']
            }

PAUSE_LIST = ['Calibrate Sound', 'Calibrate Voice']

FLUSH_LIST = ['Detect Sound', 'Detect Voice']

VALUE_LIST = ['Marker Out', 'Pulse Out', 'Pulse Time', 'Analog Out 1', 'Analog Out 2', 'Tone']

PAUSE = 1000


class RadboudboxSendControl(Item):

    def reset(self):
        self.var.command = ''
        self.var.command_value = ''

    def prepare(self):
        super().prepare()
        self._check_init()
        self._check_extended()
        self._init_var()

    def run(self):
        if self.command in VALUE_LIST:
            if isinstance(self.var.command_value,int):
                if self.var.command_value >= 0 and self.var.command_value <= 255:
                    self.command_list.append(str(self.var.command_value))
                    self.value_list.append(self.var.command_value)
                else:
                    raise OSException('Value should be between 0 and 255')
            else:
                raise OSException('Value should be an integer')

        if self.dummy_mode == 'no':
            if self.command in FLUSH_LIST:
                self._show_message('Flushing events')
                self.experiment.radboudbox.clearEvents()

            self.set_item_onset()
            self._show_message(f'Sending command: {self.command_list}')

            for value in self.value_list:
                self.experiment.radboudbox.send(value)

            if self.command in PAUSE_LIST:
                self._show_message(f'Sound/voice calibration for {PAUSE} ms')
                self.clock.sleep(PAUSE)
                self._show_message('Sound/voice calibration done!')
        elif self.dummy_mode == 'yes':
            self.set_item_onset()
            self._show_message(f'Sending command: {self.command_list}')

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose
        self.command = self.var.command
        self.command_list = list(CMD_DICT[self.command])
        self.value_list = [ord(item) for item in self.command_list]

    def _check_init(self):
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException(
                'You should have one instance of `radboudbox_init` at the start of your experiment')

    def _check_extended(self):
        if self.experiment.radboudbox_extended_mode == 'no':
            raise OSException('`radboudbox_send_control` item only works in Bitsi extended mode')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtRadboudboxSendControl(RadboudboxSendControl, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxSendControl.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):
        super().init_edit_widget()

    def apply_edit_changes(self):
        if not QtAutoPlugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()
        return True

    def edit_widget(self):
        if self.lock:
            return
        self.lock = True
        w = QtAutoPlugin.edit_widget(self)
        self.custom_interactions()
        self.lock = False
        return w

    def custom_interactions(self):
        if self.var.command in VALUE_LIST:
            self.line_edit_command_value.setEnabled(True)
        else:
            self.line_edit_command_value.setDisabled(True)



