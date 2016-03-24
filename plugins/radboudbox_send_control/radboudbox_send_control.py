#-*- coding:utf-8 -*-

"""
21-01-2016
Author: Bob Rosbag
Version: 1.0

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

#import warnings
#import os
#import imp

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin


CMD_DICT = {u'Calibrate Sound': [u'C',u'S'],
			u'Calibrate Voice': [u'C',u'V'],
			u'Detect Sound': [u'D',u'S'],
			u'Detect Voice': [u'D',u'V'],
			u'Marker Out': u'M',
			u'Pulse Out': u'P',
			u'Pulse Time': u'X',
			u'Analog Out 1': u'Y',
			u'Analog Out 2': u'Z',
			u'Tone': u'T',
			u'Analog In 1': [u'A',u'1'],
			u'Analog In 2': [u'A',u'2'],
			u'Analog In 3': [u'A',u'3'],
			u'Analog In 4': [u'A',u'4'],
			u'LEDs Off': [u'L',u'X'],
			u'LEDs Input': [u'L',u'I'],
			u'LEDs Output': [u'L',u'O']
                    }

PAUSE_LIST = [u'Calibrate Sound', u'Calibrate Voice']


class radboudbox_send_control(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox \'Send Trigger\' Plug-in'

    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values

        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        debug.msg(u'Radboud Buttonbox plug-in has been initialized!')

    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        if not hasattr(self.experiment, "radboudbox_dummy"):
            raise osexception(
                u'You should have one instance of `pygaze_init` at the start of your experiment')

        self.radboudbox_command = self.var.radboudbox_command


        self.cmd = CMD_DICT[self.radboudbox_command]
        if not isinstance(self.cmd, list):
            self.cmd = list(self.cmd)
            self.cmd.append(self.radboudbox_command_value)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

        if self.experiment.radboudbox_dummy == u'no':
            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[0])))
            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[1])))
            #debug.msg(u'Sending value %s%s to the Radboud Buttonbox' % self.cmd[0], self.cmd[1])

            if self.radboudbox_command in PAUSE_LIST:
                print(u'calibrate pause')                
                self.clock.sleep(2000)


class qtradboudbox_send_control(radboudbox_send_control, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_send_control.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
