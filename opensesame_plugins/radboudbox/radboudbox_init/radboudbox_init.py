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
import re
import sys

from libopensesame.exceptions import OSException
from libopensesame.oslogging import oslogger
from ..radboudbox_item import RadboudboxItem

# USB vendor ids of the boards in the buttonboxes: FTDI (USB UART of the
# Arduino Duemilanove, BITSI 2015), Arduino and Teensy (BITSI 2018)
BUTTONBOX_VENDOR_IDS = {0x0403, 0x2341, 0x2A03, 0x16C0}

FTDI_VENDOR_ID = 0x0403
# The FTDI chip sends small amounts of data after its latency timer (ms)
LATENCY_TIMER_MAX = 1
SYSFS_USB_SERIAL = '/sys/bus/usb-serial/devices'
LATENCY_TIMER_FIX = {
    'linux': 'echo 1 | sudo tee {sysfs} (or permanently, a udev rule: '
             'ACTION=="add", SUBSYSTEM=="usb-serial", DRIVER=="ftdi_sio", '
             'ATTR{{latency_timer}}="1")',
    'win32': 'Device Manager, Ports, {port}, Properties, Port Settings, '
             'Advanced, Latency Timer: 1 ms',
}

# Windows keeps the Advanced port settings of a USB serial port (usbser.sys,
# BITSI 2018) in its Device Parameters. Required: Use FIFO buffers off,
# receive and transmit buffer Low (1)
REGISTRY_USB = r'SYSTEM\CurrentControlSet\Enum\USB'
FIFO_SETTINGS = {'ForceFifoEnable': 0, 'RxFIFO': 1, 'TxFIFO': 1}
FIFO_SETTING_NAMES = {'ForceFifoEnable': 'Use FIFO buffers',
                      'RxFIFO': 'Receive Buffer',
                      'TxFIFO': 'Transmit Buffer'}
# What the driver uses when a setting isn't set
FIFO_SETTING_DEFAULTS = {'ForceFifoEnable': 'on', 'RxFIFO': 'High',
                         'TxFIFO': 'High'}
FIFO_SETTINGS_FIX = ('Device Manager, Ports, {port}, Properties, Port '
                     'Settings, Advanced: first set Receive Buffer and '
                     'Transmit Buffer to Low (1), then uncheck Use FIFO '
                     'buffers')

# Our lab setting for the buttonbox port on Windows: COM1-COM9
COM_NUMBER_MAX = 9
COM_NUMBER_FIX = ('Device Manager, Ports, {port}, Properties, Port '
                  'Settings, Advanced, COM Port Number: a free number below '
                  '10')

# The mode is set on the box: hold two buttons while connecting it
MODE_BUTTONS = ('BITSI 2015 (Duemilanove): A+H simple, B+H extended; '
                'BITSI 2018 (Teensy): A+E simple, B+E extended')


def usb_port_info():
    """Returns a function that gives pyserial's information on a port (also
    through a symbolic link), or None.
    """
    from serial.tools import list_ports
    usb_info = {}
    for info in list_ports.comports():
        usb_info[info.device] = info
        usb_info[os.path.realpath(info.device)] = info
    return lambda port: usb_info.get(port,
                                     usb_info.get(os.path.realpath(port)))


def read_latency_timer(info):
    """Returns the latency timer (ms) of an FTDI port and where it is set,
    or None for the timer when it can't be read.
    """
    if sys.platform.startswith('linux'):
        path = os.path.join(SYSFS_USB_SERIAL, os.path.basename(info.device),
                            'latency_timer')
        try:
            with open(path) as f:
                return int(f.read()), path
        except (OSError, ValueError):
            return None, path
    if sys.platform == 'win32':
        return read_latency_timer_windows(info), 'registry'
    return None, sys.platform


def read_latency_timer_windows(info):
    """The FTDI driver keeps the settings of each COM port in the registry:
    FTDIBUS/VID_<vid>+PID_<pid>+<serial number>/<instance>/Device Parameters
    (LatencyTimer, PortName).
    """
    import winreg

    def is_device(device, instance):
        return info.pid is not None and info.serial_number is not None \
            and device.upper() == (f'VID_{info.vid:04X}+PID_{info.pid:04X}+'
                                   f'{info.serial_number}').upper()

    parameters = find_port_parameters(r'SYSTEM\CurrentControlSet\Enum\FTDIBUS',
                                      f'VID_{info.vid:04X}+', info, is_device)
    if parameters is None:
        return None
    try:
        return int(winreg.QueryValueEx(parameters, 'LatencyTimer')[0])
    except (OSError, ValueError):
        return None


def find_port_parameters(path, prefix, info, is_device):
    """Returns the Device Parameters key of a port in the registry: the
    instance under path (HKLM, <device>/<instance>, device names that start
    with prefix) whose PortName is the port. Windows keeps the keys of devices that were connected before, and
    several can have the same PortName (two BITSI 2018 boxes both had COM4):
    then is_device(device, instance) chooses the connected one. Returns None
    when the port isn't found or can't be told apart.
    """
    import winreg
    # A key that can't be read is skipped, as a port without the values
    try:
        bus = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        devices = [winreg.EnumKey(bus, i)
                   for i in range(winreg.QueryInfoKey(bus)[0])]
    except OSError:
        return None
    found = []
    for name in devices:
        if not name.upper().startswith(prefix):
            continue
        try:
            device = winreg.OpenKey(bus, name)
            instances = [winreg.EnumKey(device, j)
                         for j in range(winreg.QueryInfoKey(device)[0])]
        except OSError:
            continue
        for instance in instances:
            try:
                parameters = winreg.OpenKey(
                    device, instance + r'\Device Parameters')
                port_name = winreg.QueryValueEx(parameters, 'PortName')[0]
            except OSError:
                continue
            if port_name.upper() == info.device.upper():
                found.append((name, instance, parameters))
    if len(found) > 1:
        found = [key for key in found if is_device(key[0], key[1])]
    return found[0][2] if len(found) == 1 else None


def read_fifo_settings_windows(info):
    """Windows keeps the settings of a USB serial port in the registry:
    USB/VID_<vid>&PID_<pid>/<serial number>/Device Parameters (PortName, and
    the Advanced port settings ForceFifoEnable, RxFIFO and TxFIFO once they
    were set). Returns these settings (None for a value that isn't set), or
    None when the port isn't found.
    """
    import winreg

    def is_device(device, instance):
        # pyserial takes the serial number from the instance (not for a
        # composite device, MI_xx, whose instance is a Windows id)
        return info.pid is not None and info.serial_number is not None \
            and device.upper() == f'VID_{info.vid:04X}&PID_{info.pid:04X}' \
            and instance.upper() == info.serial_number.upper()

    parameters = find_port_parameters(REGISTRY_USB, f'VID_{info.vid:04X}&',
                                      info, is_device)
    if parameters is None:
        return None
    settings = {}
    for setting in FIFO_SETTINGS:
        try:
            settings[setting] = winreg.QueryValueEx(parameters, setting)[0]
        except OSError:
            # Not set: the driver uses its default (on, High)
            settings[setting] = None
    return settings


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
        # rusocsci reads the ID string of the box, but doesn't keep it
        id_strings = []
        open_port = utils.open

        def open_and_keep_id(port):
            device, id_string = open_port(port)
            id_strings.append(id_string)
            return device, id_string
        utils.open = open_and_keep_id
        try:
            if self.extended_mode:
                radboudbox = extended.Extended(id=self.id, port=port)
            else:
                radboudbox = buttonbox.Buttonbox(id=self.id, port=port)
        except Exception as e:
            raise OSException(f'Could not access the Radboud Buttonbox on '
                              f'port {port}: {e}') from e
        finally:
            utils.open = open_port
        # rusocsci logs the reason and doesn't raise an exception
        if radboudbox._device is None:
            raise OSException(f'Could not open port {port} of the Radboud '
                              f'Buttonbox, see the log for the reason')
        id_string = id_strings[0] if id_strings else None
        self.experiment.radboudbox_id_string = id_string
        try:
            self._check_mode(id_string)
            self._check_latency_timer(port)
            self._check_fifo_settings(port)
            self._check_com_number(port)
        except OSException:
            radboudbox.close()
            raise
        return radboudbox

    def _check_mode(self, id_string):
        """Checks that the box is in the mode of the init item, with the ID
        string that the box sends when it starts. A box in the wrong mode
        sends wrong triggers without an error.
        """
        mode = 'extended' if self.extended_mode else 'simple'
        if id_string is None or 'Ready!' not in id_string:
            # E.g. "USB serial timeout": rusocsci didn't get it in time
            oslogger.warning(
                f'The Radboud Buttonbox did not send its ID string '
                f'({id_string!r}), so init could not check that the box is '
                f'in {mode} mode')
            return
        self._show_message(f'Radboud Buttonbox: {id_string}')
        if 'BITSI_extend mode' in id_string:
            box_mode = 'extended'
        elif 'BITSI mode' in id_string or 'BITSI event mode' in id_string:
            box_mode = 'simple'
        else:
            raise OSException(
                f"The Radboud Buttonbox is in a mode this plugin doesn't "
                f"support ('{id_string}'). Switch it to {mode} mode: hold two "
                f"buttons while connecting it ({MODE_BUTTONS})")
        if box_mode != mode:
            raise OSException(
                f"The Radboud Buttonbox is in {box_mode} mode, but Bitsi "
                f"Extended Mode in the init item is "
                f"'{'yes' if self.extended_mode else 'no'}' ({mode} mode). "
                f"Change the init item, or switch the box: hold two buttons "
                f"while connecting it ({MODE_BUTTONS})")

    def _check_latency_timer(self, port):
        """The FTDI chip of the BITSI 2015 (Duemilanove) box sends
        small amounts of data after its latency timer: 16 ms by default, so
        button presses can arrive up to 16 ms late. It should be 1 ms; on
        Windows it can change back.
        """
        info = usb_port_info()(port)
        if info is None or info.vid != FTDI_VENDOR_ID:
            return
        latency, where = read_latency_timer(info)
        self.experiment.radboudbox_latency_timer = latency
        if latency is None:
            oslogger.warning(
                f'Could not read the latency timer of the FTDI port {port} '
                f'({where}): it should be {LATENCY_TIMER_MAX} ms, otherwise '
                f'button presses can arrive up to 16 ms late')
            return
        self._show_message(f'Latency timer of {port}: {latency} ms')
        if latency > LATENCY_TIMER_MAX:
            fix = LATENCY_TIMER_FIX.get(
                'linux' if sys.platform.startswith('linux') else sys.platform,
                'set the latency timer of the FTDI driver to 1 ms')
            raise OSException(
                f'The latency timer of the Radboud Buttonbox port {port} is '
                f'{latency} ms: button presses can arrive up to {latency} ms '
                f'late. Set it to {LATENCY_TIMER_MAX} ms: '
                f'{fix.format(sysfs=where, port=info.device)}')

    def _check_fifo_settings(self, port):
        """The BITSI 2018 (Teensy) box is a USB serial port (usbser.sys) on
        Windows; our lab settings for its port are Use FIFO buffers off and
        the receive and transmit buffers Low (1).
        """
        if sys.platform != 'win32':
            return
        info = usb_port_info()(port)
        if info is None or info.vid not in BUTTONBOX_VENDOR_IDS \
                or info.vid == FTDI_VENDOR_ID:
            return
        settings = read_fifo_settings_windows(info)
        self.experiment.radboudbox_fifo_settings = settings
        fix = FIFO_SETTINGS_FIX.format(port=info.device)
        if settings is None:
            oslogger.warning(
                f'Could not read the FIFO settings of the Radboud Buttonbox '
                f'port {port}: its registry key was not found or could not '
                f'be read, or several keys have this port name and the '
                f'connected box could not be told apart. They should be: '
                f'{fix}')
            return
        self._show_message(f'FIFO settings of {port}: {settings}')
        wrong = []
        for setting, value in settings.items():
            if value == FIFO_SETTINGS[setting]:
                continue
            if value is None:
                value = (f'not set (default '
                         f'{FIFO_SETTING_DEFAULTS[setting]})')
            wrong.append(f'{FIFO_SETTING_NAMES[setting]} is {value} '
                         f'({setting})')
        if wrong:
            raise OSException(
                f'The FIFO settings of the Radboud Buttonbox port {port} are '
                f'wrong: {", ".join(wrong)}. Use FIFO buffers must be off '
                f'(0) and the buffers Low (1): {fix}')

    def _check_com_number(self, port):
        """Our lab setting for the port of both boxes on Windows: a COM
        number below 10.
        """
        if sys.platform != 'win32':
            return
        match = re.fullmatch(r'(?:\\\\\.\\)?COM(\d+)', port,
                             re.IGNORECASE)
        if match is None or int(match.group(1)) <= COM_NUMBER_MAX:
            return
        name = f'COM{match.group(1)}'
        raise OSException(
            f'The Radboud Buttonbox is on port {name}: the COM number must '
            f'be below 10. {COM_NUMBER_FIX.format(port=name)}')

    def _find_port(self, ports):
        """Chooses a port from rusocsci's list of USB serial devices (the
        device connected last first). rusocsci takes any device, e.g. the
        serial port of an audio interface, so the USB vendor id is checked.
        Autodetect takes the first buttonbox, or else the first port without
        USB data (it can't be checked); a device id takes that position.
        """
        # On Windows, rusocsci returns the port names as bytes
        ports = [p.decode() if isinstance(p, bytes) else p for p in ports]
        info = usb_port_info()

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
        self.experiment.radboudbox_id_string = None
        self.experiment.radboudbox_latency_timer = None
        self.experiment.radboudbox_fifo_settings = None

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
