#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2022

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger

CMD_DICT = {'Calibrate Sound': ['C', 'S'],
            'Calibrate Voice': ['C', 'V'],
            'Detect Sound': ['D', 'S'],
            'Detect Voice': ['D', 'V'],
            'Marker Out': 'M',
            'Pulse Out': 'P',
            'Pulse Time': 'X',
            'Analog Out 1': 'Y',
            'Analog Out 2': 'Z',
            'Tone': 'T',
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

PAUSE = 2000


class RadboudboxSendControl(Item):

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        if not isinstance(self.cmd, list):
            self.cmd = list(self.cmd)
            self.cmd.append(self.var.command)

        self.set_item_onset()
        if self.dummy_mode == 'no':
            if self.command in FLUSH_LIST:
                self._show_message('Flushing events')
                self.experiment.radboudbox.clearEvents()

            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[0])))
            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[1])))
            self._show_message('Sending command: %s' % (''.join(self.cmd)))

            if self.command in PAUSE_LIST:
                self._show_message('Sound/voice calibration for %d ms' % (PAUSE))
                self.clock.sleep(PAUSE)
                self._show_message('Sound/voice calibration done!')

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose
        self.command = self.var.command
        self.cmd = CMD_DICT[self.command]

    def _check_init(self):
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException(
                'You should have one instance of `radboudbox_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtRadboudboxSendControl(RadboudboxSendControl, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxSendControl.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

