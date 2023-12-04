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

POLL_TIME = 10


class RadboudboxGetButtonsWait(Item):

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        self._check_start()
        self.set_item_onset()
        while not self.experiment.radboudbox_get_buttons_thread_running:
            self.clock.sleep(POLL_TIME)
        if self.experiment.radboudbox_get_buttons_locked:
            self.experiment.radboudbox_get_buttons_thread.join()
        self.experiment.radboudbox_get_buttons_thread_running = 0
        self.experiment.radboudbox_get_buttons = False

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose
        self.experiment.radboudbox_get_buttons_wait = True

    def _check_init(self):
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have one instance of `radboudbox_init` at the start of your experiment')

    def _check_start(self):
        if not hasattr(self.experiment, "radboudbox_get_buttons_start"):
            raise OSException(
                    '`Radboudbox Get Buttons Start` item is missing')
        else:
            if not self.experiment.radboudbox_get_buttons:
                raise OSException(
                        'Radboudbox not waiting for a button, you first have to start the buttonbox before waiting')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)


class QtRadboudboxGetButtonsWait(RadboudboxGetButtonsWait, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxGetButtonsWait.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

