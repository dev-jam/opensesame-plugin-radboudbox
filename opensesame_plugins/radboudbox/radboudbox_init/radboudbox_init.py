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

# The FTDI driver keeps the Advanced port settings of a COM port (BITSI
# 2015) in the Device Parameters of its FTDIBUS key. ConfigData holds the
# USB transfer sizes: byte 2 transmit, byte 3 receive, as (size / 64) - 1
# (my registry exports: 0 is 64, 0x1f 2048 and 0x3f 4096 bytes)
REGISTRY_FTDIBUS = r'SYSTEM\CurrentControlSet\Enum\FTDIBUS'
FTDI_SETTINGS = {'RxTransferSize': 64, 'TxTransferSize': 64,
                 'LatencyTimer': LATENCY_TIMER_MAX, 'MinReadTimeout': 0,
                 'MinWriteTimeout': 0}
FTDI_SETTING_NAMES = {'RxTransferSize': 'Receive (Bytes)',
                      'TxTransferSize': 'Transmit (Bytes)',
                      'LatencyTimer': 'Latency Timer (msec)',
                      'MinReadTimeout': 'Minimum Read Timeout (msec)',
                      'MinWriteTimeout': 'Minimum Write Timeout (msec)'}
# A setting that isn't in the registry: the driver's default
FTDI_SETTING_DEFAULTS = {'RxTransferSize': 4096, 'TxTransferSize': 4096,
                         'LatencyTimer': 16, 'MinReadTimeout': 0,
                         'MinWriteTimeout': 0}

# Windows keeps the Advanced port settings of a USB serial port (usbser.sys,
# BITSI 2018) in its Device Parameters. Required: Use FIFO buffers off,
# receive and transmit buffer Low (1)
REGISTRY_USB = r'SYSTEM\CurrentControlSet\Enum\USB'
FIFO_SETTINGS = {'ForceFifoEnable': 0, 'RxFIFO': 1, 'TxFIFO': 1}
FIFO_SETTING_NAMES = {'ForceFifoEnable': 'Use FIFO buffers',
                      'RxFIFO': 'Receive Buffer',
                      'TxFIFO': 'Transmit Buffer'}
# A setting that was never changed in the Device Manager isn't in the
# registry: its default (Use FIFO buffers on, buffers High)
FIFO_SETTING_DEFAULTS = {'ForceFifoEnable': 1, 'RxFIFO': 14, 'TxFIFO': 16}

# Our lab setting for the buttonbox port on Windows: COM1-COM9
COM_NUMBER_MAX = 9
COM_NUMBER_FIX = ('Device Manager, Ports, {port}, Properties, Port '
                  'Settings, Advanced, COM Port Number: a free number below '
                  '10')

# The error that lists the port settings of a box on Windows. OpenSesame
# shows it as Markdown (and as text in the console): blank lines between
# paragraphs, indented lines keep their line breaks
PORT_SETTINGS_CURRENT = (
    'The port settings of the Radboud Buttonbox on {port} are wrong:\n\n'
    'Current settings are:\n\n'
    '{current}\n\n')
PORT_SETTINGS_MESSAGE = PORT_SETTINGS_CURRENT + (
    'Please go to:\n\n'
    '    Device Manager > Ports (COM & LPT) > {device} > Port Settings > '
    'Advanced\n\n'
    '{fix}')
PORT_SETTINGS_FIX_2018 = (
    'Set the following when incorrect, the order is important!\n\n'
    '1. First set "COM Port Number" to a COM port below 10.\n'
    '2. Then set both "Receive Buffer" and "Transmit Buffer" to "Low (1)", '
    'by moving the sliders all the way to the left.\n'
    '3. Finally, uncheck "Use FIFO buffers".\n\n'
    'Now you should see:\n\n'
    '    Port: COM3 (or another COM port below 10)\n'
    '    Use FIFO buffers: off\n'
    '    Receive Buffer: Low (1)\n'
    '    Transmit Buffer: Low (1)')
PORT_SETTINGS_FIX_2015 = (
    'Set the following when incorrect:\n\n'
    '    Port: COM3 (or another COM port below 10)\n'
    '    Receive (Bytes): 64\n'
    '    Transmit (Bytes): 64\n'
    '    Latency Timer (msec): 1\n'
    '    Minimum Read Timeout (msec): 0\n'
    '    Minimum Write Timeout (msec): 0\n\n'
    'Leave the other settings as they are.')

# Linux: the latency timer of the BITSI 2015 is in sysfs, written by the
# ftdi_sio driver; the chip starts at 16 ms when it is connected
PORT_SETTINGS_MESSAGE_LINUX = PORT_SETTINGS_CURRENT + (
    'Please run:\n\n'
    '    echo 1 | sudo tee {sysfs}\n\n'
    'This lasts until the box is disconnected. To set it permanently, add '
    'a udev rule, then disconnect and reconnect the box:\n\n'
    '    echo \'ACTION=="add", SUBSYSTEM=="usb-serial", DRIVER=="ftdi_sio", '
    'ATTR{{latency_timer}}="1"\' | sudo tee '
    '/etc/udev/rules.d/99-ftdi-latency-timer.rules\n'
    '    sudo udevadm control --reload-rules\n\n'
    'Now you should see:\n\n'
    '    cat {sysfs}\n'
    '    1')

# Linux: ModemManager probes a new cdc_acm port whose interface says it
# takes modem (AT) commands (protocol 1-6), as the Teensy (BITSI 2018) does:
# it opens the port and sends commands to the box. It ignores a device with
# ID_MM_DEVICE_IGNORE=1 on the USB device or on the port (its mm-filter.c),
# set by udev rules; udev keeps the properties of each device in its
# database, /run/udev/data/c<major>:<minor>
PROC = '/proc'
SYSFS_TTY = '/sys/class/tty'
UDEV_DATA = '/run/udev/data'
MODEM_MANAGER_WARNING = (
    'ModemManager is running and may use the Radboud Buttonbox on {port}: '
    'when the box is connected, ModemManager can open its port and send '
    'modem commands to it. To make ModemManager ignore the box, run:\n\n'
    '    echo \'ATTRS{{idVendor}}=="{vid:04x}", '
    'ENV{{ID_MM_DEVICE_IGNORE}}="1", '
    'ENV{{ID_MM_PORT_IGNORE}}="1"\' | sudo tee '
    '/etc/udev/rules.d/99-radboudbox-modemmanager.rules\n'
    '    sudo udevadm control --reload-rules\n\n'
    'then disconnect and reconnect the box. For a Teensy, the udev rules '
    'of PJRC (https://www.pjrc.com/teensy/00-teensy.rules) do the same. Or '
    'remove ModemManager when you don\'t use a modem.')

# Log variables radboudbox_<name>, set by init: NA in dummy mode and for
# settings that the box or the system doesn't have, unknown when they can't
# be read
LOG_VARIABLES = (
    'type', 'port', 'driver', 'id_string', 'port_settings',
    # BITSI 2015 (latency timer also on Linux)
    'latency_timer', 'receive_bytes', 'transmit_bytes', 'min_read_timeout',
    'min_write_timeout',
    # BITSI 2018: Windows, Linux
    'use_fifo_buffers', 'receive_buffer', 'transmit_buffer', 'modemmanager')
FTDI_LOG_VARIABLES = {'LatencyTimer': 'latency_timer',
                      'RxTransferSize': 'receive_bytes',
                      'TxTransferSize': 'transmit_bytes',
                      'MinReadTimeout': 'min_read_timeout',
                      'MinWriteTimeout': 'min_write_timeout'}
FIFO_LOG_VARIABLES = {'ForceFifoEnable': 'use_fifo_buffers',
                      'RxFIFO': 'receive_buffer',
                      'TxFIFO': 'transmit_buffer'}
WRONG_PORT_SETTINGS_WARNING = (
    '\n\nWrong port settings is set to warning in the init item: the '
    'experiment continues.')

# The mode is set on the box: hold two buttons while connecting it
MODE_BUTTONS = ('BITSI 2015 (Duemilanove): A+H simple, B+H extended; '
                'BITSI 2018 (Teensy): A+E simple, B+E extended')


def com_number(port):
    """Returns the number of a Windows COM port (COM12 or \\\\.\\COM12),
    or None for another name.
    """
    match = re.fullmatch(r'(?:\\\\\.\\)?COM(\d+)', port, re.IGNORECASE)
    return None if match is None else int(match.group(1))


def device_manager_name(info, default):
    """The name of a port in the Device Manager, e.g. USB Serial Device
    (COM4): pyserial's description is the device's friendly name.
    """
    if info.description and info.device in info.description:
        return info.description
    return f'{default} ({info.device})'


def port_settings_lines(settings):
    """Lines of (name, value, correct) for the error; correct is None when
    the setting could not be read.
    """
    return '\n'.join(
        f'    {name}: {value}' + (
            '' if correct is None
            else f' ({"correct" if correct else "incorrect"})')
        for name, value, correct in settings)


def modem_manager_running():
    """Whether a ModemManager process runs."""
    try:
        pids = [pid for pid in os.listdir(PROC) if pid.isdigit()]
    except OSError:
        return False
    for pid in pids:
        try:
            with open(os.path.join(PROC, pid, 'comm')) as f:
                if f.read().strip() == 'ModemManager':
                    return True
        except OSError:
            continue
    return False


def probed_by_modem_manager(port):
    """Whether ModemManager would probe the port: the protocol of its USB
    interface says modem (AT) commands (1-6). The tty is in sysfs at
    <interface>/tty/<name>. False when that can't be read.
    """
    tty = os.path.join(SYSFS_TTY, os.path.basename(os.path.realpath(port)))
    interface = os.path.dirname(os.path.dirname(os.path.realpath(tty)))
    try:
        with open(os.path.join(interface, 'bInterfaceProtocol')) as f:
            return 1 <= int(f.read(), 16) <= 6
    except (OSError, ValueError):
        return False


def ignored_by_modem_manager(port):
    """Whether udev set ID_MM_DEVICE_IGNORE=1 on the port's tty or on the
    USB device above it (the devices in sysfs with a device number), as
    udev rules for the Teensy do.
    """
    path = os.path.realpath(os.path.join(
        SYSFS_TTY, os.path.basename(os.path.realpath(port))))
    while path not in ('/', '/sys', '/sys/devices', ''):
        try:
            with open(os.path.join(path, 'dev')) as f:
                device_id = f'c{f.read().strip()}'
            with open(os.path.join(UDEV_DATA, device_id)) as f:
                if 'E:ID_MM_DEVICE_IGNORE=1' in f.read().splitlines():
                    return True
        except OSError:
            pass
        path = os.path.dirname(path)
    return False


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
    return None, sys.platform


def read_ftdi_settings_windows(info):
    """The FTDI driver keeps the settings of each COM port in the registry:
    FTDIBUS/VID_<vid>+PID_<pid>+<serial number>/<instance>/Device Parameters
    (PortName, LatencyTimer, MinReadTimeout, MinWriteTimeout, and the USB
    transfer sizes in ConfigData). Returns these settings (the default for
    a value that isn't there, None for transfer sizes that can't be read),
    or None when the port isn't found.
    """
    import winreg
    parameters = find_port_parameters(REGISTRY_FTDIBUS, f'VID_{info.vid:04X}+',
                                      info, is_ftdibus_device(info))
    if parameters is None:
        return None
    settings = dict(FTDI_SETTING_DEFAULTS)
    for setting in ('LatencyTimer', 'MinReadTimeout', 'MinWriteTimeout'):
        try:
            settings[setting] = winreg.QueryValueEx(parameters, setting)[0]
        except OSError:
            pass
    try:
        config = winreg.QueryValueEx(parameters, 'ConfigData')[0]
    except OSError:
        config = None
    if config is not None:
        if isinstance(config, bytes) and len(config) >= 4:
            settings['TxTransferSize'] = (config[2] + 1) * 64
            settings['RxTransferSize'] = (config[3] + 1) * 64
        else:
            settings['TxTransferSize'] = settings['RxTransferSize'] = None
    return settings


def is_usb_device(info):
    """Returns is_device() for find_port_key() under Enum\\USB: pyserial
    takes the serial number from the instance (not for a composite device,
    MI_xx, whose instance is a Windows id).
    """
    def is_device(device, instance):
        return info.pid is not None and info.serial_number is not None \
            and device.upper() == f'VID_{info.vid:04X}&PID_{info.pid:04X}' \
            and instance.upper() == info.serial_number.upper()
    return is_device


def is_ftdibus_device(info):
    """Returns is_device() for find_port_key() under Enum\\FTDIBUS: the
    serial number is in the device name.
    """
    def is_device(device, instance):
        return info.pid is not None and info.serial_number is not None \
            and device.upper() == (f'VID_{info.vid:04X}+PID_{info.pid:04X}+'
                                   f'{info.serial_number}').upper()
    return is_device


def find_port_key(path, prefix, info, is_device):
    """Returns the registry key of a port: the instance under path (HKLM,
    <device>/<instance>, device names that start with prefix) whose
    Device Parameters have the port as PortName. Windows keeps the keys of
    devices that were connected before, and several can have the same
    PortName (two BITSI 2018 boxes both had COM4): then
    is_device(device, instance) chooses the connected one. Returns None
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
                found.append((name, instance, device))
    if len(found) > 1:
        found = [key for key in found if is_device(key[0], key[1])]
    if len(found) != 1:
        return None
    try:
        return winreg.OpenKey(found[0][2], found[0][1])
    except OSError:
        return None


def find_port_parameters(path, prefix, info, is_device):
    """Returns the Device Parameters key of a port (see find_port_key()),
    or None.
    """
    import winreg
    key = find_port_key(path, prefix, info, is_device)
    if key is None:
        return None
    try:
        return winreg.OpenKey(key, 'Device Parameters')
    except OSError:
        return None


def read_driver(info):
    """Returns the name of the port's driver (e.g. ftdi_sio or cdc_acm on
    Linux, FTSER2K or usbser on Windows), or None.
    """
    if sys.platform.startswith('linux'):
        driver = os.path.join(SYSFS_TTY,
                              os.path.basename(os.path.realpath(info.device)),
                              'device', 'driver')
        if not os.path.exists(driver):
            return None
        return os.path.basename(os.path.realpath(driver))
    if sys.platform != 'win32':
        return None
    import winreg
    if info.vid == FTDI_VENDOR_ID:
        key = find_port_key(REGISTRY_FTDIBUS, f'VID_{info.vid:04X}+', info,
                            is_ftdibus_device(info))
    else:
        key = find_port_key(REGISTRY_USB, f'VID_{info.vid:04X}&', info,
                            is_usb_device(info))
    if key is None:
        return None
    try:
        return str(winreg.QueryValueEx(key, 'Service')[0])
    except OSError:
        return None


def read_fifo_settings_windows(info):
    """Windows keeps the settings of a USB serial port in the registry:
    USB/VID_<vid>&PID_<pid>/<serial number>/Device Parameters (PortName, and
    the Advanced port settings ForceFifoEnable, RxFIFO and TxFIFO once they
    were changed in the Device Manager). Returns these settings (the default
    for a value that isn't set), or None when the port isn't found.
    """
    import winreg
    parameters = find_port_parameters(REGISTRY_USB, f'VID_{info.vid:04X}&',
                                      info, is_usb_device(info))
    if parameters is None:
        return None
    settings = {}
    for setting in FIFO_SETTINGS:
        try:
            settings[setting] = winreg.QueryValueEx(parameters, setting)[0]
        except OSError:
            # Never changed: the default (on, High)
            settings[setting] = FIFO_SETTING_DEFAULTS[setting]
    return settings


class RadboudboxInit(RadboudboxItem):

    def reset(self):
        self.var.dummy_mode = 'no'
        self.var.verbose = 'yes'
        self.var.id = 'autodetect'
        self.var.port = 'autodetect'
        self.var.extended_mode = 'yes'
        self.var.wrong_port_settings = 'error'

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
        self._log('id_string', id_string)
        try:
            self._check_mode(id_string)
            self._check_port_settings(port)
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

    def _check_port_settings(self, port):
        """Checks the settings of the buttonbox port: the latency timer
        (FTDI), and on Windows our lab settings (COM number, and for the
        BITSI 2018 the FIFO buffers). On Windows one error lists all
        settings of the box. On Linux, a warning when ModemManager may use
        the BITSI 2018. The box, its port and its settings are logged.
        """
        info = usb_port_info()(port)
        self._log('port', port if info is None else info.device)
        self._log('driver', None if info is None else read_driver(info))
        if info is not None and info.vid == FTDI_VENDOR_ID:
            self._log('type', 'BITSI 2015')
            self._check_latency_timer(port, info)
        elif info is not None and info.vid in BUTTONBOX_VENDOR_IDS:
            self._log('type', 'BITSI 2018')
            if sys.platform == 'win32':
                self._check_fifo_settings(port, info)
            elif sys.platform.startswith('linux'):
                # No port settings on Linux (cdc_acm)
                self._log('port_settings', 'correct')
                self._check_modem_manager(port, info)
            else:
                self._log('port_settings', None)
        else:
            self._log('type', None)
            self._check_com_number(port)

    def _log(self, name, value):
        """Sets the log variable radboudbox_<name>; None is unknown."""
        self.experiment.var.set(f'radboudbox_{name}',
                                'unknown' if value is None else value)

    def _port_settings_status(self, settings):
        """Logs whether the settings (name, value, correct) are correct, and
        returns True when one of them is incorrect.
        """
        corrects = [correct for _, _, correct in settings]
        if False in corrects:
            status = 'incorrect'
        elif None in corrects:
            status = None
        else:
            status = 'correct'
        self._log('port_settings', status)
        return status == 'incorrect'

    def _wrong_port_settings(self, message):
        """An error, or a warning when the init item says so."""
        if self.wrong_port_settings == 'warning':
            oslogger.warning(message + WRONG_PORT_SETTINGS_WARNING)
            return
        raise OSException(message)

    def _check_modem_manager(self, port, info):
        """The BITSI 2018 (Teensy) says it takes modem commands: a running
        ModemManager opens its port when it is connected, unless udev rules
        make it ignore the box.
        """
        if not modem_manager_running():
            self._log('modemmanager', 'not running')
            return
        if not probed_by_modem_manager(port) \
                or ignored_by_modem_manager(port):
            self._log('modemmanager', 'does not use the box')
            return
        self._log('modemmanager', 'may use the box')
        oslogger.warning(MODEM_MANAGER_WARNING.format(port=info.device,
                                                      vid=info.vid))

    def _port_row(self, info):
        number = com_number(info.device)
        return 'Port', info.device, number is None or \
            number <= COM_NUMBER_MAX

    def _check_latency_timer(self, port, info):
        """The FTDI chip of the BITSI 2015 (Duemilanove) box sends
        small amounts of data after its latency timer: 16 ms by default, so
        button presses can arrive up to 16 ms late. It should be 1 ms; on
        Windows it can change back.
        """
        if sys.platform == 'win32':
            self._check_ftdi_settings(port, info)
            return
        latency, where = read_latency_timer(info)
        self.experiment.radboudbox_latency_timer = latency
        self._log('latency_timer', latency)
        if latency is None:
            self._log('port_settings', None)
            oslogger.warning(
                f'Could not read the latency timer of the FTDI port {port} '
                f'({where}): it should be {LATENCY_TIMER_MAX} ms, otherwise '
                f'button presses can arrive up to 16 ms late')
            return
        self._show_message(f'Latency timer of {port}: {latency} ms')
        # Only Linux has a value here (sysfs)
        settings = [('Latency Timer (msec)', latency,
                     latency <= LATENCY_TIMER_MAX)]
        if self._port_settings_status(settings):
            self._wrong_port_settings(PORT_SETTINGS_MESSAGE_LINUX.format(
                port=info.device, sysfs=where,
                current=port_settings_lines(settings)))

    def _check_ftdi_settings(self, port, info):
        """The BITSI 2015 (FTDI) box on Windows: the latency timer (see
        above) and our lab settings for its port, a COM number below 10, USB
        transfer sizes of 64 bytes and minimum read and write timeouts of 0.
        """
        ftdi = read_ftdi_settings_windows(info)
        self.experiment.radboudbox_ftdi_settings = ftdi
        latency = None if ftdi is None else ftdi['LatencyTimer']
        self.experiment.radboudbox_latency_timer = latency
        device = device_manager_name(info, 'USB Serial Port')
        if ftdi is None:
            oslogger.warning(
                f'Could not read the settings of the FTDI port {port} from '
                f'the registry: its key was not found or could not be read, '
                f'or several keys have this port name and the connected box '
                f'could not be told apart. The latency timer should be '
                f'{LATENCY_TIMER_MAX} ms, otherwise button presses can arrive '
                f'up to 16 ms late (Device Manager > Ports (COM & LPT) > '
                f'{device} > Port Settings > Advanced)')
        else:
            self._show_message(f'FTDI settings of {port}: {ftdi}')
        settings = [self._port_row(info)]
        for setting, required in FTDI_SETTINGS.items():
            value = None if ftdi is None else ftdi[setting]
            self._log(FTDI_LOG_VARIABLES[setting], value)
            if value is None:
                settings.append((FTDI_SETTING_NAMES[setting],
                                 'could not be read', None))
                continue
            if setting == 'LatencyTimer':
                correct = isinstance(value, int) and 1 <= value <= required
            else:
                correct = value == required
            settings.append((FTDI_SETTING_NAMES[setting], value, correct))
        if self._port_settings_status(settings):
            self._wrong_port_settings(PORT_SETTINGS_MESSAGE.format(
                port=info.device, current=port_settings_lines(settings),
                device=device, fix=PORT_SETTINGS_FIX_2015))

    def _check_fifo_settings(self, port, info):
        """The BITSI 2018 (Teensy) box is a USB serial port (usbser.sys) on
        Windows; our lab settings for its port are a COM number below 10,
        Use FIFO buffers off and the receive and transmit buffers Low (1).
        """
        fifo = read_fifo_settings_windows(info)
        self.experiment.radboudbox_fifo_settings = fifo
        device = device_manager_name(info, 'USB Serial Device')
        if fifo is None:
            oslogger.warning(
                f'Could not read the FIFO settings of the Radboud Buttonbox '
                f'port {port}: its registry key was not found or could not '
                f'be read, or several keys have this port name and the '
                f'connected box could not be told apart. They should be: '
                f'Use FIFO buffers off, Receive Buffer and Transmit Buffer '
                f'Low (1) (Device Manager > Ports (COM & LPT) > {device} > '
                f'Port Settings > Advanced)')
        else:
            self._show_message(f'FIFO settings of {port}: {fifo}')
        settings = [self._port_row(info)]
        for setting in FIFO_SETTINGS:
            if fifo is None:
                self._log(FIFO_LOG_VARIABLES[setting], None)
                settings.append((FIFO_SETTING_NAMES[setting],
                                 'could not be read', None))
                continue
            value = fifo[setting]
            if setting == 'ForceFifoEnable':
                shown = {0: 'off', 1: 'on'}.get(value, value)
            else:
                shown = 'Low (1)' if value == 1 else value
            self._log(FIFO_LOG_VARIABLES[setting],
                      shown if setting == 'ForceFifoEnable' else value)
            settings.append((FIFO_SETTING_NAMES[setting], shown,
                             value == FIFO_SETTINGS[setting]))
        if self._port_settings_status(settings):
            self._wrong_port_settings(PORT_SETTINGS_MESSAGE.format(
                port=info.device, current=port_settings_lines(settings),
                device=device, fix=PORT_SETTINGS_FIX_2018))

    def _check_com_number(self, port):
        """Our lab setting for the port on Windows, also when it isn't
        known which box it is: a COM number below 10. The other settings of
        such a port are unknown.
        """
        self._log('port_settings', None)
        if sys.platform != 'win32':
            return
        number = com_number(port)
        if number is None or number <= COM_NUMBER_MAX:
            return
        self._log('port_settings', 'incorrect')
        name = f'COM{number}'
        self._wrong_port_settings(
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
        wrong_port_settings = self.var.wrong_port_settings
        if wrong_port_settings not in ('error', 'warning'):
            raise OSException(f"Wrong port settings should be 'error' or "
                              f"'warning', not '{wrong_port_settings}'")
        self.wrong_port_settings = wrong_port_settings
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
        self.experiment.radboudbox_ftdi_settings = None
        # Log variables: NA until the box is checked (and in dummy mode)
        for name in LOG_VARIABLES:
            self.experiment.var.set(f'radboudbox_{name}', 'NA')

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
