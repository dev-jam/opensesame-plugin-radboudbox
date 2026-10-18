# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dev-jam/opensesame-plugin-radboudbox/compare/5.0.0...HEAD
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
