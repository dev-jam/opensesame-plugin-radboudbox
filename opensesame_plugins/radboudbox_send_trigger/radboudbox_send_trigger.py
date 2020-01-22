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

VERSION = u'2020.01-1'

class radboudbox_send_trigger(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox: sends a trigger.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        self.var.value = 0


    def init_var(self):

        """Set en check variables."""

        if hasattr(self.experiment, "radboudbox_dummy_mode"):
            self.dummy_mode = self.experiment.radboudbox_dummy_mode
            self.verbose = self.experiment.radboudbox_verbose
        else:
            raise osexception(
                    u'You should have one instance of `radboudbox_init` at the start of your experiment')


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.init_var()


    def run(self):

        """Run phase"""

        self.value = self.var.value

        if self.dummy_mode == u'no':
            ## turn trigger on
            #self.experiment.radboudbox.clearEvents()
            self.set_item_onset()
            self.experiment.radboudbox.sendMarker(val=self.value)
            debug.msg(u'Sending value %s to the Radboud Buttonbox' % self.value)
        elif self.dummy_mode == u'yes':
            debug.msg(u'Dummy mode enabled, NOT sending value %s to the Radboud Buttonbox' % self.value)
        else:
           debug.msg(u'Error with dummy mode')


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtradboudbox_send_trigger(radboudbox_send_trigger, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_send_trigger.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
