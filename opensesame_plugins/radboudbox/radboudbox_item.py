"""
This file is part of opensesame-plugin-radboudbox.

Copyright (C) 2016-2026 Bob Rosbag <mail@bobrosbag.nl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

SPDX-License-Identifier: GPL-3.0-or-later
"""

__author__ = "Bob Rosbag"
__license__ = "GPL-3.0-or-later"

from libopensesame.base_response_item import BaseResponseItem
from libopensesame.exceptions import OSException
from libopensesame.item import Item
from libopensesame.oslogging import oslogger
from openexp.keyboard import Keyboard


class RadboudboxItem(Item):
    """Base class of the Radboud Buttonbox items."""

    def _check_init(self):
        """Checks for the init item and reads its settings."""
        if not hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have one instance of `radboudbox_init` at the start of your experiment')
        self.dummy_mode = self.experiment.radboudbox_dummy_mode == 'yes'
        self.verbose = self.experiment.radboudbox_verbose == 'yes'

    def _show_message(self, message):
        oslogger.debug(message)
        if self.verbose:
            print(message)


class RadboudboxResponseItem(RadboudboxItem, BaseResponseItem):
    """Base class of the items that collect button responses. In dummy mode,
    the keyboard is used instead.

    The item collects up to number_of_responses responses within the
    timeout (infinite: all responses until the timeout). The first one is
    the response of the item (response_<item>, response_time_<item>,
    correct_<item>, time_response_<item>); all of them are logged in
    responses_<item> and their timestamps in time_responses_<item>,
    separated by ';' ('NA' when there was none).
    """

    def reset(self):
        self.var.timeout = 'infinite'
        self.var.number_of_responses = 1

    def prepare(self):
        self._check_init()
        super().prepare()
        # rusocsci's waitButtons() fails with a timeout of 0
        if self._timeout == 0:
            raise OSException("Timeout should be more than 0 ms or 'infinite'")
        self._number_of_responses = self._prepare_number_of_responses()

    def _prepare_number_of_responses(self):
        """Returns the number of responses to collect, or None to collect
        them until the timeout.
        """
        value = self.var.number_of_responses
        if value == 'infinite':
            if self._timeout is None:
                raise OSException("Number of responses 'infinite' needs a "
                                  "timeout: with timeout 'infinite' the item "
                                  "would wait forever")
            return None
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise OSException(f"Number of responses should be a whole number "
                              f"of 1 or more, or 'infinite', not '{value}'")
        return value

    def prepare_response_func(self):
        if self.dummy_mode:
            self._keyboard = Keyboard(self.experiment,
                                      keylist=self._allowed_responses,
                                      timeout=self._timeout)
            return self._keyboard.get_key

    def process_response(self, response_args):
        response, t1 = response_args
        self.experiment.var.set(f'time_response_{self.name}', t1)
        if not response:
            response = 'NA'
        elif isinstance(response, list):
            response = response[0]
        super().process_response((response, t1))
        response_time = round(t1 - self._t0, 1)
        self._show_message(f"Detected press on button: '{response}'")
        self._show_message(f"Response time: {response_time} ms")

    def _collect_dummy_response(self):
        self._show_message('Dummy mode on, using keyboard')
        self._keyboard.flush()
        self._collect_responses(self._collect_response,
                                lambda remaining: self._keyboard.get_key(
                                    keylist=self._allowed_responses,
                                    timeout=remaining))

    def _collect_responses(self, wait_first, wait_next):
        """Collects the responses and processes them. wait_first() waits
        for the first response with the item's timeout, wait_next(remaining)
        for the next one, with the rest of the timeout in ms (None: no
        timeout); both return (response, timestamp), with response None
        after a timeout.
        """
        start = self.clock.time()
        response, t1 = wait_first()
        responses = []
        while response is not None:
            responses.append((response, t1))
            if self._number_of_responses is not None and \
                    len(responses) >= self._number_of_responses:
                break
            remaining = None
            if self._timeout is not None:
                remaining = self._timeout - (self.clock.time() - start)
                if remaining <= 0:
                    break
            response, t1 = wait_next(remaining)
        # The first response is the response of the item
        self.process_response(responses[0] if responses else (None, t1))
        self._log_responses(responses)

    def _log_responses(self, responses):
        if responses:
            keys = ';'.join(str(response) for response, _ in responses)
            # A whole number as OpenSesame logs time_response_<item>
            times = ';'.join(str(int(t)) if float(t).is_integer() else str(t)
                             for _, t in responses)
        else:
            keys = times = 'NA'
        self.experiment.var.set(f'responses_{self.name}', keys)
        self.experiment.var.set(f'time_responses_{self.name}', times)
        if len(responses) > 1:
            self._show_message(f"Detected {len(responses)} responses: {keys}")

    def _wait_until_unlocked(self):
        """Waits until a collect buttons bg start item has its response. The
        thread is joined, not polled: clock.sleep() of the legacy backend
        holds up the other threads, which made the response time of the
        thread late.
        """
        if self.experiment.radboudbox_get_buttons_locked:
            self.experiment.radboudbox_get_buttons_thread.join()

    def _wait_buttons(self):
        """Waits for the buttons and processes the responses. The box
        sends every press and release; the timestamp of each is the moment
        it is read. Only the first wait flushes the input.
        """
        if self._timeout is None:
            timeout = float('inf')
        else:
            timeout = self._timeout / 1000
        self._collect_responses(
            lambda: self._wait_button(timeout, flush=True),
            lambda remaining: self._wait_button(
                float('inf') if remaining is None else remaining / 1000,
                flush=False))

    def _wait_button(self, timeout, flush):
        try:
            response = self.experiment.radboudbox.waitButtons(
                maxWait=timeout, buttonList=self._allowed_responses,
                flush=flush)
        except UnboundLocalError:
            # rusocsci 0.9.2 raises this when the timeout has passed before
            # its first read (its loop never runs): no response
            response = None
        except ValueError as e:
            # Or pyserial's, when the timeout passes between rusocsci's
            # check and its setting of the read timeout (negative)
            if not str(e).startswith('Not a valid timeout'):
                raise
            response = None
        t1 = self.clock.time()
        return (response[0] if response else None), t1
