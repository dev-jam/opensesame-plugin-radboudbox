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


class radboudbox_init(item):

    """
    This class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox \'Send Trigger\' Plug-in'

    def reset(self):

        """Resets plug-in to initial values."""

        # Set default experimental variables and values
        self.var.radboudbox_dummy = u'no'
        self.var.id = u'autodetect'
        self.var.port = u'autodetect'

        # Debugging output is only visible when OpenSesame is started with the
        # --debug argument.
        debug.msg(u'Radboud Buttonbox plug-in has been initialized!')

    def prepare(self):

        """Preparation phase"""

        # Call the parent constructor.
        item.prepare(self)

        self.radboudbox_dummy = self.var.radboudbox_dummy        
        self.id = self.var.id
        self.port = self.var.port  
        if self.id == u'autodetect':
            self.id = 0
        if self.port == u'autodetect':
            self.port = None
        if self.radboudbox_dummy == u'no':
            try:
                from rusocsci import buttonbox
                print(buttonbox.__file__ )
            except ImportError:
                debug.msg(u'The RuSocSci package could not be loaded. Check if the file is present and if the file permissions are correct.')

            if not hasattr(self.experiment, "radboudbox"):
                            
                
                try:
                    self.experiment.radboudbox = buttonbox.Buttonbox(id=self.id, port=self.port)
                except OSError:
                    debug.msg(u'Could not access the Radboud Buttonbox')
        elif self.radboudbox_dummy == u'yes':
            debug.msg(u'Dummy mode enabled, prepare phase')
        else:
            debug.msg(u'Error with dummy mode, dummy mode: %s' % self.var.radboudbox_dummy)

    def run(self):

        """Run phase"""

        # self.set_item_onset() sets the time_[item name] variable. Optionally,
        # you can pass a timestamp, such as returned by canvas.show().


    def close(self):

        """
        desc:
            Neatly close the connection to the buttonbox.
        """

        if not hasattr(self.experiment, "radboudbox") or \
            self.experiment.radboudbox is None:
                debug.msg("no active radboudbox")
                return
        try:
            self.experiment.radboudbox.close()
            self.experiment.radboudbox = None
            debug.msg("radboudbox closed")
        except:
            debug.msg("failed to close radboudbox")


class qtradboudbox_init(radboudbox_init, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        """Plug-in GUI"""

        radboudbox_init.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
