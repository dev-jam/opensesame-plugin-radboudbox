# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [5.4.0] - 2026-10-30

- init has a new setting, *Wrong port settings*: *error* (the default, as before) stops the experiment when a port setting is wrong; *warning* writes the same text as a warning in the log, and the experiment continues
- init logs the box and its port settings: `radboudbox_type`, `radboudbox_port`, `radboudbox_driver`, `radboudbox_id_string`, `radboudbox_port_settings` (correct, incorrect or unknown), and the settings themselves (latency timer, transfer sizes, timeouts, FIFO buffers, ModemManager); `NA` in dummy mode and for settings the box or system doesn't have

## [5.3.0] - 2026-10-29

- the latency timer error on Linux has the layout of the port settings error on Windows: the current value, the command that sets it, a udev rule that sets it permanently, and how to check it
- on Linux, init warns when ModemManager runs and may use the BITSI 2018: the Teensy says it takes modem commands, so ModemManager opens its port when it is connected, unless a udev rule makes it ignore the box (`ID_MM_DEVICE_IGNORE`); the warning gives such a rule

## [5.2.0] - 2026-10-29

- init raises an error on Windows when the port of a BITSI 2018 (Teensy, a USB serial port) has Use FIFO buffers on, or a receive or transmit buffer other than Low (1) (registry values `ForceFifoEnable`, `RxFIFO` and `TxFIFO` of the port; a value that is not in the registry, because it was never changed, counts as its default: FIFO buffers on, buffers High (14 and 16)); the settings are read from the registry key of the connected box (by its USB serial number), also when another box had the same COM port name; a warning when the port's registry key can't be read or the connected box can't be told apart. The values are on the experiment as `radboudbox_fifo_settings`
- init raises an error on Windows when the buttonbox port (both types) is COM10 or higher
- on Windows, init lists all port settings of the box in one error, on several lines: COM port number and latency timer (BITSI 2015), COM port number and FIFO buffers (BITSI 2018), each marked correct or incorrect, with where to change them in the Device Manager and what to set The latency timer error on Linux is unchanged
- fixed: on Windows, the latency timer of a BITSI 2015 was read from the registry key of another box when two boxes had the same COM port name; it is read from the key of the connected box (by its USB serial number), and a warning when it can't be told apart. A registry key that can't be read is a warning instead of "An unexpected error occurred" (since 5.1.0)
- init raises an error on Windows when the port of a BITSI 2015 (FTDI) has USB transfer sizes other than 64 bytes (Receive and Transmit) or minimum read or write timeouts other than 0; they are in the port settings error with the latency timer. A latency timer that is not in the registry counts as the driver's default of 16 ms (an error; it was a warning). The values are on the experiment as `radboudbox_ftdi_settings`

## [5.1.2] - 2026-10-22

- fixed: send control Pulse Out and Pulse Time were an error on a BITSI 2015 with the 2015-11-18 firmware (ID string `BITSI_extend mode, Ready! 2015-11-18`), which has them (tested); they are now only an error with the 2014 firmware, whose ID string ends with `Ready!`
- readme: the BITSI 2018 Duemilanove is not a separate box, but the BITSI 2015 with the 2018 firmware; the three firmware versions of the BITSI 2015 and their ID strings, and the send control commands tested with the 2015-11-18 firmware
- init: the mode buttons in the error message name the boxes as BITSI 2015 (Duemilanove) and BITSI 2018 (Teensy)

## [5.1.1] - 2026-10-21

- fixed: a wait buttons item that waits for get buttons start to finish joins its thread instead of checking every ms; with the legacy backend, these checks held up the thread, and its response time came out 10-20 ms late (also in 4.6.0 and earlier)
- fixed: on Windows, a registry key of an FTDI device that can't be read made init fail with "An unexpected error occurred"; it is skipped, as intended (a warning when the latency timer can't be read)
- changed: in dummy mode, `time_response_<item>` is the time of the key press, as `response_time` is; it was taken after processing the response (up to 1 ms later in tests)
- code style: indentation and line length (no change in behavior)
- readme: the name of the developer of RuSocSci (Wilbert van Ham)

## [5.1.0] - 2026-10-21

- fixed: port autodetect takes the first buttonbox (FTDI, Arduino or Teensy USB device) instead of the device connected last; it took, for example, the serial port of an audio interface, and the experiment ran without the buttonbox (also in 4.6.0 and earlier)
- a device id that points to another USB device is an error that names the device and the buttonboxes found
- pyserial is a declared dependency (init uses it directly; rusocsci already installed it)
- fixed: init raises an error when the box is in another mode (simple or extended, set on the box itself) than Bitsi Extended Mode in the init item; before, triggers and commands were sent wrong without an error. The check uses the ID string the box sends at the start; without it, there is a warning in the log
- the ID string of the box is on the experiment as `radboudbox_id_string` (None when it didn't arrive)
- fixed: send control Tone sends no value; the box reads Tone as one character, so the value was read as the start of a new command (e.g. 77 turned the next command into a marker)
- send control Pulse Out and Pulse Time are an error on a box with the 2015 firmware (when its ID string arrived): it doesn't have them, and may read the value as a new command
- send control Analog In 1-4 reads the number the box sends back and logs it as `analog_in_<item name>` (NA in dummy mode); before, the answer was not read. An error when the box doesn't answer within 200 ms, or while get buttons start collects buttons in the background
- readme: the buttonbox types (BITSI 2015, BITSI 2018 Duemilanove and Teensy), how to set their mode, port autodetect, and which send control commands each type supports
- init raises an error when the latency timer of an FTDI port (BITSI 2015 and 2018 Duemilanove) is more than 1 ms: button presses could arrive up to 16 ms late. Read from sysfs on Linux and from the registry on Windows; a warning when it can't be read. The value is on the experiment as `radboudbox_latency_timer`

## [5.0.1] - 2026-10-18

- the help texts of the controls are shown next to them (`info`); the `tooltip` texts were never shown, because OpenSesame ignores that key
- the help text of the device id no longer says it is a device name: it is a number (0 is the device connected last), used with port autodetect

## [5.0.0] - 2026-10-18

- fixed: init raises an error when the buttonbox can't be found or opened, instead of continuing (later items failed with an unclear error, or the experiment ran without the box)
- fixed: init raises an error when rusocsci is missing, for an invalid dummy mode or bitsi extended mode, and for a device id that is not a number (with port autodetect)
- fixed: a second init item is an error in dummy mode too
- fixed: get buttons start and wait work in dummy mode (the wait item always failed)
- fixed: an error while collecting buttons in the background (e.g. a lost connection) is raised by the get buttons wait item; before, it was ignored and a later wait buttons item waited forever
- fixed: a timeout of 0 is an error (rusocsci's waitButtons() fails with it)
- fixed: send control gives a clear error for an empty or unknown command (was a KeyError)
- fixed: send trigger error messages for the pulse time
- code shared by the items is in `radboudbox_item.py`; no `py3compat`; only send trigger and send control have a GUI class
- changed: init no longer prints "No active radboudbox" at the start (it did even with verbose off)
- changed: a failure to close the buttonbox at the end of the experiment is a warning in the log
- changed: each setting is read once (this only matters for a setting with an expression)
- changed: get buttons start continues up to 1 ms sooner (it no longer polls for the start of the thread)
- the version label of the items reads the version from the installed package (set only in `pyproject.toml`)
- license metadata is the SPDX identifier `GPL-3.0-or-later` (it was the file `LICENSE.md`, which is removed; the license text is in `COPYING`)
- requires Python 3.10 or later
- readme: rusocsci is installed with the plug-in (there is no shipped copy), dummy mode
- changed: send trigger and send control set the onset (`time_<item>`) right after sending, and print their messages afterwards ("Sent ..."), so a slow console can't delay the trigger or the end of the pulse
- changed: in dummy mode, send trigger logs `time_<item>` and waits for the pulse time, and send control waits for the sound/voice calibration (1000 ms), as with the buttonbox

## [4.6.0] - 2025-09-28

- only create keyboard item in dummy mode (fixes all kinds of multi-threading problems)
- more precise placement of lock
- bg item always join the thread

## [4.5.0] - 2025-09-19

- reorganization of code to make it more robust

## [4.4.0] - 2025-09-05

- convert string handling to f-strings

## [4.3.0] - 2025-09-03

- wait_buttons, get_buttons_wait: moved timeout to run stage
- code cleanup

## [4.2.0] - 2025-07-17

- license cleanup

## [4.1.1] - 2024-06-03

- add 1 ms pause after start thread to compensate for initialization of buttonbox
    
## [4.1.0] - 2024-05-24

- enable pulse mode
    
## [4.0.0] - 2024-05-23

- code improvement for send control item and send trigger item
- checkbox bitsi simple and extended
    
## [3.1.0] - 2023-12-04

- fixed item dependency checks when running an experiment
    
## [3.0.1] - 2023-08-30

- fixed dependencies
    
## [3.0.0] - 2023-08-15

- new style api OpenSesame 4.0
- lots of small fixes and code cleanup
    
## [2.5.0] - 2023-08-13

Final release for OpenSesame 3 API

- small bugfixes
    
## [v2.4.0] - 2023-07-03

- removed some legacy code, multiprocessing with spawn on Linux should work now.
    
## [v2.3.0] - 2022-11-25

- new plugin code style
- debian packaging fixed

## v2.0.0 - 2021-04-15

- First release

[Unreleased]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.4.0...HEAD
[5.4.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.3.0...5.4.0
[5.3.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.2.0...5.3.0
[5.2.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.1.2...5.2.0
[5.1.2]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.1.1...5.1.2
[5.1.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.1.0...5.1.1
[5.1.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.0.1...5.1.0
[5.0.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.0.0...5.0.1
[5.0.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.6.0...5.0.0
[4.6.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.5.0...4.6.0
[4.5.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.4.0...4.5.0
[4.4.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.3.0...4.4.0
[4.3.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.2.0...4.3.0
[4.2.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.1.1...4.2.0
[4.1.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.1.0...4.1.1
[4.1.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/4.0.0...4.1.0
[4.0.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.1.0...4.0.0
[3.1.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.0.1...3.1.0
[3.0.1]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/3.0.0...3.0.1
[3.0.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/2.5.0...3.0.0
[2.5.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.4.0...2.5.0
[v2.4.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.3.0...v2.4.0
[v2.3.0]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/v2.0.0...v2.3.0
