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
from libopensesame.oslogging import oslogger
from ..radboudbox_item import RadboudboxItem


class RadboudboxInit(RadboudboxItem):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'yes'
        self.var.id = 'autodetect'
        self.var.port = 'autodetect'
        self.var.extended_mode = 'yes'

    def prepare(self):
        super().prepare()
        self._check_single_init()
        self._init_var()
        if self.dummy_mode:
            self._show_message('Dummy mode enabled, prepare phase')
            return
        self.experiment.radboudbox = self._open()
        self.clock.sleep(4000)
        self.experiment.cleanup_functions.append(self.close)

    def run(self):
        self.set_item_onset()

    def close(self):
        if getattr(self.experiment, 'radboudbox', None) is None:
            self._show_message("No active radboudbox")
            return
        try:
            self.experiment.radboudbox.clearEvents()
            self.experiment.radboudbox.close()
            self.experiment.radboudbox = None
            self._show_message("Radboudbox closed")
        except Exception as e:
            # Cleanup also runs after an error: raising would hide it
            oslogger.warning(f'Failed to close the Radboud Buttonbox: {e}')

    def _open(self):
        try:
            from rusocsci import buttonbox, extended, utils
        except ImportError as e:
            raise OSException('The RuSocSci package could not be imported. '
                              'Please install it: pip install rusocsci') from e
        port = self.port
        if port is None:
            port = utils.getPort(self.id)
            if port is None:
                raise OSException(
                    f'Could not find the Radboud Buttonbox: no USB serial '
                    f'device with device id {self.id} (0 is the device '
                    f'connected last)')
            # On Windows, rusocsci returns the port name as bytes
            if isinstance(port, bytes):
                port = port.decode()
        try:
            if self.extended_mode:
                radboudbox = extended.Extended(id=self.id, port=port)
            else:
                radboudbox = buttonbox.Buttonbox(id=self.id, port=port)
        except Exception as e:
            raise OSException(f'Could not access the Radboud Buttonbox on '
                              f'port {port}: {e}') from e
        # rusocsci logs the reason and doesn't raise an exception
        if radboudbox._device is None:
            raise OSException(f'Could not open port {port} of the Radboud '
                              f'Buttonbox, see the log for the reason')
        return radboudbox

    def _check_single_init(self):
        if hasattr(self.experiment, 'radboudbox_dummy_mode'):
            raise OSException('You should have only one instance of `radboudbox_init` in your experiment')

    def _init_var(self):
        dummy_mode = self.var.dummy_mode
        extended_mode = self.var.extended_mode
        verbose = self.var.verbose
        if dummy_mode not in ('yes', 'no'):
            raise OSException(f"Dummy mode should be 'yes' or 'no', not "
                              f"'{dummy_mode}'")
        if extended_mode not in ('yes', 'no'):
            raise OSException(f"Bitsi extended mode should be 'yes' or 'no', "
                              f"not '{extended_mode}'")
        self.dummy_mode = dummy_mode == 'yes'
        self.extended_mode = extended_mode == 'yes'
        self.verbose = verbose == 'yes'
        # Shared with the other items (and inline scripts): keep names and types
        self.experiment.radboudbox_extended_mode = extended_mode
        self.experiment.radboudbox_dummy_mode = dummy_mode
        self.experiment.radboudbox_verbose = verbose
        self.experiment.radboudbox_get_buttons_locked = 0
        self.experiment.radboudbox_get_buttons = None

        device_id = self.var.id
        port = self.var.port
        self.id = 0 if device_id == 'autodetect' else device_id
        if port == 'autodetect':
            self.port = None
            # The device id is only used to choose a port
            if not isinstance(self.id, int):
                raise OSException(
                    f"Device id should be a number (0 is the device connected "
                    f"last) or 'autodetect', not '{self.id}'. Use Port for a "
                    f"port name")
        else:
            self.port = str(port)
