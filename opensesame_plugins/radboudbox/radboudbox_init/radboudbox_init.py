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

import os

from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from ..radboudbox_item import RadboudboxItem

# USB vendor ids of the boards in the buttonboxes: FTDI (USB UART of the
# Arduino Duemilanove), Arduino and Teensy (BITSI 2018)
BUTTONBOX_VENDOR_IDS = {0x0403, 0x2341, 0x2A03, 0x16C0}


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
            port = self._find_port(utils.serialList())
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

    def _find_port(self, ports):
        """Chooses a port from rusocsci's list of USB serial devices (the
        device connected last first). rusocsci takes any device, e.g. the
        serial port of an audio interface, so the USB vendor id is checked.
        Autodetect takes the first buttonbox, or else the first port without
        USB data (it can't be checked); a device id takes that position.
        """
        from serial.tools import list_ports
        # On Windows, rusocsci returns the port names as bytes
        ports = [p.decode() if isinstance(p, bytes) else p for p in ports]
        usb_info = {}
        for info in list_ports.comports():
            usb_info[info.device] = info
            usb_info[os.path.realpath(info.device)] = info

        def info(port):
            return usb_info.get(port, usb_info.get(os.path.realpath(port)))

        def is_other_device(port):
            return info(port) is not None and info(port).vid is not None \
                and info(port).vid not in BUTTONBOX_VENDOR_IDS

        def describe(ports):
            return ', '.join(
                f'{p} ({info(p).description}, {info(p).hwid})'
                if info(p) is not None else p for p in ports) or 'none'

        boxes = [p for p in ports if not is_other_device(p)]
        others = [p for p in ports if is_other_device(p)]
        if not ports:
            raise OSException('Could not find the Radboud Buttonbox: no USB '
                              'serial device found')
        if self.id is None:
            if boxes:
                return boxes[0]
            raise OSException(
                f'Could not find the Radboud Buttonbox. Other USB serial '
                f'devices: {describe(others)}')
        if not -len(ports) <= self.id < len(ports):
            raise OSException(
                f'Could not find the Radboud Buttonbox: no USB serial device '
                f'with device id {self.id} (0 is the device connected last). '
                f'USB serial devices: {describe(ports)}')
        port = ports[self.id]
        if is_other_device(port):
            raise OSException(
                f'Could not find the Radboud Buttonbox: device id {self.id} '
                f'is another USB device: {describe([port])}. Buttonboxes: '
                f'{describe(boxes)}')
        return port

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
        # None: the first buttonbox found
        self.id = None if device_id == 'autodetect' else device_id
        if port == 'autodetect':
            self.port = None
            # The device id is only used to choose a port
            if self.id is not None and not isinstance(self.id, int):
                raise OSException(
                    f"Device id should be a number (0 is the device connected "
                    f"last) or 'autodetect', not '{device_id}'. Use Port for "
                    f"a port name")
        else:
            self.port = str(port)
