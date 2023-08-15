#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2020

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


class RadboudboxSendTrigger(Item):

    def reset(self):
        self.var.value = 0

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        if self.dummy_mode == 'no':
            self.set_item_onset()
            self.experiment.radboudbox.sendMarker(val=self.var.value)
            self._show_message('Sending value %s to the Radboud Buttonbox' % self.var.value)
        elif self.dummy_mode == 'yes':
            self._show_message('Dummy mode enabled, NOT sending value %s to the Radboud Buttonbox' % self.var.value)
        else:
            self._show_message('Error with dummy mode')

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose

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
