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
from libopensesame.base_response_item import BaseResponseItem
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard


class RadboudboxWaitButtons(BaseResponseItem):

    def reset(self):
        self.var.timeout = 'infinite'

    def prepare(self):
        super().prepare()
        self._check_init()
        self._init_var()

    def run(self):
        self._show_message('Start collecting buttons')
        self._start_buttons()

    def prepare_response_func(self):
        self._keyboard = Keyboard(self.experiment,
                                  keylist=self._allowed_responses,
                                  timeout=self._timeout)
        if self.experiment.radboudbox_dummy_mode == 'yes':
            return self._keyboard.get_key

    def _start_buttons(self):
        if self.dummy_mode == 'no':
            self._t0 = self.set_item_onset()
            resp = self.experiment.radboudbox.waitButtons(maxWait=self._timeout,
                                                          buttonList=self._allowed_responses,
                                                          flush=self.flush)
            t1 = self.clock.time()
            self._set_response_time()
            if not resp:
                resp = 'NA'
            elif isinstance(resp, list):
                resp = resp[0]
            retval = resp, t1
            response_time = round(t1 - self._t0, 1)
            self.process_response(retval)
            self._show_message("Detected press on button: '%s'" % resp)
            self._show_message("Response time: %s ms" % response_time)
        else:
            self._keyboard.flush()
            super().run()
            self._set_response_time()

    def _init_var(self):
        self.dummy_mode = self.experiment.radboudbox_dummy_mode
        self.verbose = self.experiment.radboudbox_verbose
        self.flush = True
        if self.dummy_mode == 'no':
            if self._timeout == 'infinite' or self._timeout == None:
                self._timeout = float("inf")
            else:
                self._timeout = float(self._timeout) / 1000
        self._t0 = None

    def _check_init(self):
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have one instance of `radboudbox_init` at the start of your experiment')

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose == 'yes':
            print(message)

    def _set_response_time(self, time=None):
        if time is None:
            time = self.clock.time()
        self.experiment.var.set('time_response_%s' % self.name, time)
        return time


class QtRadboudboxWaitButtons(RadboudboxWaitButtons, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxWaitButtons.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)
