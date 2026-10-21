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

__author__ = "Bob Rosbag"
__license__ = "GPLv3"

from libopensesame.exceptions import OSException
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from ..radboudbox_item import RadboudboxItem

CMD_DICT = {'Calibrate Sound': ['C', 'S'],
            'Calibrate Voice': ['C', 'V'],
            'Detect Sound': ['D', 'S'],
            'Detect Voice': ['D', 'V'],
            'Marker Out': ['M'],
            'Pulse Out': ['P'],
            'Pulse Time': ['X'],
            'Analog Out 1': ['Y'],
            'Analog Out 2': ['Z'],
            'Tone': ['T'],
            'Analog In 1': ['A', '1'],
            'Analog In 2': ['A', '2'],
            'Analog In 3': ['A', '3'],
            'Analog In 4': ['A', '4'],
            'LEDs Off': ['L', 'X'],
            'LEDs Input': ['L', 'I'],
            'LEDs Output': ['L', 'O']
            }

PAUSE_LIST = ['Calibrate Sound', 'Calibrate Voice']

FLUSH_LIST = ['Detect Sound', 'Detect Voice']

# Tone is one character: a value after it would be read as a new command
VALUE_LIST = ['Marker Out', 'Pulse Out', 'Pulse Time', 'Analog Out 1', 'Analog Out 2']

# Only in the 2018 firmware, whose ID string has a version (" w:2018")
FIRMWARE_2018_LIST = ['Pulse Out', 'Pulse Time']

PAUSE = 1000

# The box answers Analog In with a number (2018 firmware: with a line end)
ANALOG_IN_LIST = ['Analog In 1', 'Analog In 2', 'Analog In 3', 'Analog In 4']
ANALOG_IN_TIMEOUT = 200  # (ms) for the answer
ANALOG_IN_QUIET = 20  # (ms) without a new digit: the answer is complete


class RadboudboxSendControl(RadboudboxItem):

    def reset(self):
        self.var.command = ''
        self.var.command_value = ''

    def prepare(self):
        super().prepare()
        self._check_init()
        if self.experiment.radboudbox_extended_mode == 'no':
            raise OSException('`radboudbox_send_control` item only works in Bitsi extended mode')
        self.command = self.var.command
        if self.command not in CMD_DICT:
            raise OSException(f"Unknown command '{self.command}', choose one "
                              f"of: {', '.join(CMD_DICT)}")
        # The 2015 firmware ignores the command, and may read its value as
        # the start of a new command
        id_string = self.experiment.radboudbox_id_string
        if self.command in FIRMWARE_2018_LIST and id_string is not None \
                and 'Ready!' in id_string and ' w:' not in id_string:
            raise OSException(
                f"'{self.command}' needs a buttonbox with the 2018 firmware; "
                f"this box has an older one ('{id_string}'). For a pulse, use "
                f"Send Trigger with pulse mode")

    def run(self):
        command_list = CMD_DICT[self.command]
        value_list = [ord(item) for item in command_list]
        if self.command in VALUE_LIST:
            # The value may be set by an earlier item
            value = self.var.command_value
            if not isinstance(value, int):
                raise OSException('Value should be an integer')
            if not 0 <= value <= 255:
                raise OSException('Value should be between 0 and 255')
            command_list = command_list + [str(value)]
            value_list.append(value)

        # The messages come after sending. Dummy mode also pauses for the
        # calibration, so the timing is the same.
        if not self.dummy_mode:
            if self.command in ANALOG_IN_LIST:
                # The answer comes on the port of the buttons
                if self.experiment.radboudbox_get_buttons_locked:
                    raise OSException(
                        f"'{self.command}' can't be read while Get Buttons "
                        f"Start collects buttons in the background: put it "
                        f"after Get Buttons Wait")
                self.experiment.radboudbox.clearEvents()
            if self.command in FLUSH_LIST:
                self.experiment.radboudbox.clearEvents()
            for value in value_list:
                self.experiment.radboudbox.send(value)
        self.set_item_onset()
        if self.dummy_mode:
            self._show_message(f'Dummy mode enabled, NOT sending command: {command_list}')
        else:
            if self.command in FLUSH_LIST:
                self._show_message('Flushed events')
            self._show_message(f'Sent command: {command_list}')
        if self.command in ANALOG_IN_LIST:
            value = 'NA' if self.dummy_mode else self._read_analog_in()
            self.experiment.var.set(f'analog_in_{self.name}', value)
            self._show_message(f'{self.command}: {value}')
        if self.command in PAUSE_LIST:
            self._show_message(f'Sound/voice calibration for {PAUSE} ms')
            self.clock.sleep(PAUSE)
            self._show_message('Sound/voice calibration done!')

    def _read_analog_in(self):
        """Reads the number the box sends after Analog In, with rusocsci's
        waitButtons(): digits and the line end only, so button presses in
        between are skipped (the next wait for buttons flushes them anyway).
        """
        allowed = list('0123456789\n')
        digits = ''
        t_end = self.clock.time() + ANALOG_IN_TIMEOUT
        while True:
            # The 2015 firmware sends no line end: after the first digit, a
            # short silence ends the answer
            wait = ANALOG_IN_QUIET if digits else t_end - self.clock.time()
            if wait <= 0:
                break
            character = self.experiment.radboudbox.waitButtons(
                maxWait=wait / 1000, buttonList=allowed, flush=False)
            if character is None or character[0] == '\n':
                break
            digits += character[0]
        if not digits:
            raise OSException(f"The Radboud Buttonbox did not answer "
                              f"'{self.command}' within {ANALOG_IN_TIMEOUT} "
                              f"ms")
        return int(digits)


class QtRadboudboxSendControl(RadboudboxSendControl, QtAutoPlugin):

    def __init__(self, name, experiment, script=None):
        RadboudboxSendControl.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def apply_edit_changes(self):
        if not super().apply_edit_changes():
            return False
        self._update_command_value()
        return True

    def edit_widget(self):
        widget = super().edit_widget()
        self._update_command_value()
        return widget

    def _update_command_value(self):
        """Enables the value field only for commands that take a value."""
        self.line_edit_command_value.setEnabled(
            self.var.command in VALUE_LIST)
