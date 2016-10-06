#-*- coding:utf-8 -*-

"""
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

from libopensesame.exceptions import osexception
from libopensesame import debug
from libqtopensesame.items.qtautoplugin import qtautoplugin
import openexp.keyboard
from libopensesame.py3compat import *
from libopensesame.item import item
from libopensesame.generic_response import generic_response


class radboudbox_get_buttons(item, generic_response):

    """
    desc:
        A plug-in for using the serial response box.
    """

    def reset(self):

        """
        desc:
            Reset item and experimental variables.
        """

        self.var.timeout = u'infinite'
        #self.var.lights = u''
        #self.var.require_state_change = u'no'
        #self.process_feedback = True

    def prepare(self):

        """
        desc:
            Prepare the item.
        """

        if not hasattr(self.experiment, "radboudbox_dummy"):
            raise osexception(
                u'You should have one instance of `pygaze_init` at the start of your experiment')

        self.timeout = self.var.timeout

        item.prepare(self)
        self.prepare_timeout()
        self._require_state_change = False
 
        # Prepare the allowed responses
        self._allowed_responses = None
        if u'allowed_responses' in self.var:
            self._allowed_responses = []
            for r in safe_decode(self.var.allowed_responses).split(u';'):
                if r.strip() != u'':
                    self._allowed_responses.append(r)
            if not self._allowed_responses:
                self._allowed_responses = None
        debug.msg(u"allowed responses set to %s" % self._allowed_responses)
        print(u"allowed responses set to %s" % self._allowed_responses)

        # Prepare keyboard for dummy-mode and flushing
        self._keyboard = openexp.keyboard.keyboard(self.experiment)
        if self.experiment.radboudbox_dummy == u'yes':
            self._resp_func = self._keyboard.get_key
            return
        else:
            if self.timeout == u'infinite' or self.timeout == None:
                self._timeout = float("inf")
            else:
                self._timeout = self.timeout

        # Prepare auto response
        if self.experiment.auto_response:
            self._resp_func = self.auto_responder
        else:
            self._resp_func = self.experiment.radboudbox.waitButtons

    def run(self):

        """
        desc:
            Runs the item.
        """

        self.set_item_onset()
        self._keyboard.flush()
        self.set_sri(reset=True)
        if self.experiment.radboudbox_dummy == 'yes':
            # In dummy mode, we simply take the numeric keys from the keyboard
            if self._allowed_responses is None:
                self._allowed_responses = list(range(0,10))
            resp, self.experiment.end_response_interval = self._resp_func(
                keylist=self._allowed_responses, timeout=self._timeout)
        else:
            # Get the response
            try:
                #self.experiment.radboudbox.clearEvents()
                [resp] = self._resp_func(maxWait=self._timeout, buttonList=self._allowed_responses)
                self.experiment.end_response_interval   = self.clock.time()
                self.experiment.var.button_detect_time  = self.experiment.end_response_interval
            except Exception as e:
                raise osexception(
                    "An error occured in radboudbox '%s': %s." % (self.name, e))
            if isinstance(resp, list):
                resp = resp[0]
        print("Detected press on button: '%s'" % resp)
        debug.msg("received %s" % resp)
        self.experiment.var.response = resp
        generic_response.response_bookkeeping(self)

    def var_info(self):

        """
        returns:
            A list of (name, description) tuples with variable descriptions.
        """

        return item.var_info(self) + \
            generic_response.var_info(self)


class qtradboudbox_get_buttons(radboudbox_get_buttons, qtautoplugin):

    def __init__(self, name, experiment, script=None):

        radboudbox_get_buttons.__init__(self, name, experiment, script)
        qtautoplugin.__init__(self, __file__)
