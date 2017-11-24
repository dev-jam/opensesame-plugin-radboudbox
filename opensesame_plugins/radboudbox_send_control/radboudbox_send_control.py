#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2017

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

#import warnings
#import os
#import imp

from libopensesame.py3compat import *
from libopensesame import debug
from libopensesame.item import item
from libqtopensesame.items.qtautoplugin import qtautoplugin
from libopensesame.exceptions import osexception

VERSION = u'2017.11-1'

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

FLUSH_LIST = [u'Detect Sound', u'Detect Voice']

PAUSE = 2000

class radboudbox_send_control(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox: sends a control command to the buttonbox.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        pass

    def init_var(self):

        """Set en check variables."""

        if hasattr(self.experiment, "radboudbox_dummy_mode"):
            self.dummy_mode = self.experiment.radboudbox_dummy_mode
            self.verbose = self.experiment.radboudbox_verbose
        else:
            raise osexception(
                    u'You should have one instance of `radboudbox_init` at the start of your experiment')

        self.command = self.var.command
        self.cmd = CMD_DICT[self.command]


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.init_var()


    def run(self):

        """Run phase"""

        if not isinstance(self.cmd, list):
            self.cmd = list(self.cmd)
            self.cmd.append(self.var.command)

        self.set_item_onset()
        if self.dummy_mode == u'no':
            if self.command in FLUSH_LIST:
                self.show_message(u'Flushing events')
                self.experiment.radboudbox.clearEvents()

            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[0])))
            self.experiment.radboudbox.sendMarker(val=(ord(self.cmd[1])))
            self.show_message(''.join(self.cmd))

            if self.command in PAUSE_LIST:
                self.show_message(u'Calibration pause')
                self.clock.sleep(PAUSE)


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtradboudbox_send_control(radboudbox_send_control, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_send_control.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
        self.text_version.setText(
        u'<small>Parallel Port Trigger version %s</small>' % VERSION)
