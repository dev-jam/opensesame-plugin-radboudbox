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

from libopensesame.exceptions import osexception
from libopensesame import debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.keyboard import keyboard
from libopensesame.py3compat import *
from libopensesame.item import item


VERSION = u'2017.11-1'

class radboudbox_get_buttons_wait(item):

    """
    Class handles the basic functionality of the item.
    It does not deal with GUI stuff.
    """

    # Provide an informative description for your plug-in.
    description = u'Radboud Buttonbox: waits until the background button registration has finished.'

    def __init__(self, name, experiment, string=None):

        item.__init__(self, name, experiment, string)
        self.verbose = u'no'
        self.poll_time = 10


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

        self.experiment.radboudbox_get_buttons_wait = 1


    def prepare(self):

        """
        desc:
            Prepare the item.
        """

        item.prepare(self)
        self.prepare_timeout()

        # create keyboard object
        #self.kb = keyboard(self.experiment,timeout=1)

        self.init_var()


    def run(self):

        """Run phase"""

        self.set_item_onset()

        if not hasattr(self.experiment, "radboudbox_get_buttons_start"):
            raise osexception(
                    u'Radboudbox Get Buttons Start item is missing')

        if self.dummy_mode == u'no':

            ## wait if thread has not started yet
            while not self.experiment.radboudbox_get_buttons_thread_running:
                self.clock.sleep(self.poll_time)

            ## join thread if thread is still running
            if self.experiment.radboudbox_get_buttons_locked:
                self.experiment.radboudbox_get_buttons_thread.join()

            ## set end of thread
            self.experiment.radboudbox_get_buttons_thread_running = 0

        elif self.dummy_mode == u'yes':
            self.show_message(u'Dummy mode enabled, NOT playing audio')
        else:
            self.show_message(u'Error with dummy mode!')


    def show_message(self, message):
        """
        desc:
            Show message.
        """

        debug.msg(message)
        if self.verbose == u'yes':
            print(message)


class qtradboudbox_get_buttons_wait(radboudbox_get_buttons_wait, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        radboudbox_get_buttons_wait.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
        self.text_version.setText(
        u'<small>Parallel Port Trigger version %s</small>' % VERSION)
