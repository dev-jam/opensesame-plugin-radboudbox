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


class radboudbox_send_trigger(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox \'Send Trigger\' Plug-in'

    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.radboudbox_value = 0

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

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().

        self.radboudbox_value = self.var.radboudbox_value

        if self.experiment.radboudbox_dummy == u'no':
            ## turn trigger on
            #self.experiment.radboudbox.clearEvents()
            self.experiment.radboudbox.sendMarker(val=self.radboudbox_value)
            self.experiment.var.trigger_code = self.radboudbox_value
            debug.msg(u'Sending value %s to the Radboud Buttonbox' % self.radboudbox_value)
        elif self.experiment.radboudbox_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, NOT sending value %s to the Radboud Buttonbox' % self.radboudbox_value)
        else:
           debug.msg(u'Error with dummy mode')


class qtradboudbox_send_trigger(radboudbox_send_trigger, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_send_trigger.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
