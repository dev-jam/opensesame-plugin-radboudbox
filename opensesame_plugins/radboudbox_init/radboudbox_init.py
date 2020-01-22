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

class radboudbox_init(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox - initializes the buttonbox.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'


    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.dummy_mode = u'no'
        self.var.verbose = u'no'
        self.var.id = u'autodetect'
        self.var.port = u'autodetect'

        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        self.show_message(u'Radboud Buttonbox plug-in has been initialized!')


    def init_var(self):

        """Set en check variables."""

        self.dummy_mode = self.var.dummy_mode
        self.verbose = self.var.verbose
        self.experiment.radboudbox_dummy_mode = self.var.dummy_mode
        self.experiment.radboudbox_verbose = self.var.verbose
        self.experiment.radboudbox_get_buttons_locked = 0
        self.experiment.radboudbox_get_buttons_wait = None
        self.experiment.radboudbox_get_buttons_start = None

        if self.var.id == u'autodetect':
            self.id = 0
        else:
            self.id = self.var.id

        if self.var.port == u'autodetect':
            self.port = None
        else:
            self.port = self.var.port

        if hasattr(self.experiment, "radboudbox"):
            raise osexception(
                    u'You should have only one instance of `radboudbox_init` in your experiment')


    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)
        self.close()
        self.init_var()

        if self.dummy_mode == u'no':
            try:
                from rusocsci import buttonbox
            except ImportError:
                self.show_message(u'The RuSocSci package could not be imported. Please install package.')
            try:
                self.experiment.radboudbox = buttonbox.Buttonbox(id=self.id, port=self.port)
                self.clock.sleep(4000)
                self.experiment.cleanup_functions.append(self.close)
                self.python_workspace[u'radboudbox'] = self.experiment.radboudbox
            except OSError:
                    debug.msg(u'Could not access the Radboud Buttonbox')
        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled, prepare phase')
        else:
            self.show_message(u'Error with dummy mode, dummy mode: %s' % self.dummy_mode)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().
        self.set_item_onset()


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


    def close(self):

        """
        desc:
            Neatly close the connection to the buttonbox.
        """

        if not hasattr(self.experiment, "radboudbox") or \
            self.experiment.radboudbox is None:
                self.show_message("no active radboudbox")
                return
        try:
            self.experiment.radboudbox.clearEvents()
            self.experiment.radboudbox.close()
            self.experiment.radboudbox = None
            self.show_message("radboudbox closed")
        except:
            self.show_message("failed to close radboudbox")


class qtradboudbox_init(radboudbox_init, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)

