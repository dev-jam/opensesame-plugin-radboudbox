OpenSesame Plug-in: Radboud Buttonbox
==========

*An OpenSesame plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2022, Bob Rosbag

This plugin makes use of the RuSocSci python package developed by Wilbert van Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 
  
  
## About

The Technical Support Group (Radboud University, Social Sciences) developed a USB Arduino based Buttonbox which can be used for time accurate (1ms) button press, voice key, sound key registration and sending parallel port like triggers.
Upper case A, B, C, D, E (, F, G, H) are used for key presses, and lower case a, b, c, d, e (, f, g, h) are used for key releases. Uppercase S is used for sound key detection and uppercase V for voice key.

For more information:

<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>


This plug-in consists of foreground and background (multithreaded) items.


Difference between foreground and background:

- **Foreground** item starts button/signal registration until it detects an allowed button or the set duration has passed. 
- **Background** item consist of a 'start' and 'wait' item. These are fully multi-threaded. After the start of the button/signal registration, the item will immediately advance to the next item. When the experiment reaches the 'wait' item, it will wait until a button/signal has been detected by the 'start' item or the duration has passed.


This plug-in has six items:

- **Init** initialization of the buttonbox, this should be placed at the beginning of an experiment.
- **Wait Buttons** waits for a button press or release before continuing to the next item in the experiment
- **Get Buttons Start** starts a new thread which monitors for button presses/releases, it will directly advance to the next item in the experiment
- **Get Buttons Wait** waits until the thread from 'Get Buttons Start' is finished (has detected a button press/release) before advancing to the next item in the experiment 
- **Send Control** send control code to the buttonbox, for example 'Calibrate Sound', 'Detect Sound'
- **Send Trigger** for sending triggers to hardware with a parallel port


Timestamps can be found in the logs by the name: time_response_[item_name]


In **dummy mode** (an option of the Init item) the plug-in runs without a buttonbox: the keyboard is used for button responses, and triggers and commands are not sent. Get Buttons Start then waits for the key press itself, because the keyboard can't be read in the background.


Linux and Windows are supported (possibly also macOS, not tested). The plug-in needs OpenSesame 4 (Python 3.10 or later) and the [RuSocSci](https://pypi.org/project/RuSocSci/) package, which is installed with it:

    pip install opensesame-plugin-radboudbox
  
  
## Buttonboxes

| | BITSI 2015 | BITSI 2018 |
|---|---|---|
| Board | Arduino Duemilanove, FTDI USB (0403:6001) | Teensy 3.6 (USB vendor 16C0) |
| Port on Linux | /dev/ttyUSB*, /dev/serial/by-id/usb-FTDI_* | /dev/ttyACM* |
| Simple mode | hold A+H while connecting | hold A+E while connecting |
| Extended mode | hold B+H while connecting | hold B+E while connecting |

**Firmware.** The BITSI 2015 runs one of three firmware versions; the ID string it sends when it starts (extended mode) tells which:

| Box | Firmware | ID string (extended mode) |
|---|---|---|
| BITSI 2015 | 2014 | `BITSI_extend mode, Ready!` |
| BITSI 2015 | 2015-11-18 | `BITSI_extend mode, Ready! 2015-11-18` |
| BITSI 2015 | 2018 | `BITSI_extend mode, Ready! w:2018` |
| BITSI 2018 | 2018 (Teensy) | `BITSI_extend mode, Ready! w:2018` |

The sources of the 2014 and 2018 firmware, for the Duemilanove and the Teensy, are in the Buttonbox downloads of the [TSG](https://tsgdoc.socsci.ru.nl/index.php/ButtonBox); the 2018 Duemilanove firmware uses the same pins as the 2014 firmware. The source of the 2015-11-18 firmware is not in these downloads.

**Mode.** The box stores its mode (simple or extended) itself. *Bitsi Extended Mode* in the Init item must match it: a box in the other mode sends wrong triggers. Init checks this with the ID string the box sends when it starts, and raises an error when the modes differ. When the ID string doesn't arrive in time, the mode can't be checked; there is a warning in the log.

**Port.** With port *autodetect*, Init takes the first buttonbox it finds (an FTDI, Arduino or Teensy USB device). Other USB serial devices, such as the serial port of an audio interface, are skipped. A *Device id* takes that position in the list of USB serial devices (0 is the device connected last). To choose a port yourself, set *Port*, e.g. `/dev/ttyUSB0` or `COM3`.

**Latency timer.** The FTDI chip of the BITSI 2015 sends small amounts of data after its latency timer, 16 ms by default: button presses can then arrive up to 16 ms late. It must be 1 ms, and Init raises an error otherwise. On Windows, set it in the Device Manager (Ports, the COM port, Properties, Port Settings, Advanced, Latency Timer); it can change back, e.g. after a driver update. On Linux it is `/sys/bus/usb-serial/devices/ttyUSB0/latency_timer`. The Teensy box has no latency timer.

**FIFO buffers (Windows).** On Windows, the BITSI 2018 (Teensy) is a USB serial port (driver usbser.sys). Its port must have *Use FIFO buffers* off and the receive and transmit buffers at Low (1). Set them in the Device Manager (Ports, the COM port, Properties, Port Settings, Advanced): first set *Receive Buffer* and *Transmit Buffer* to Low (1), then uncheck *Use FIFO buffers*; unchecked first, the buffers stay at their values, greyed out. Init reads them from the registry (`ForceFifoEnable`, `RxFIFO` and `TxFIFO` in the port's `Device Parameters`) and raises an error when one of them is different. A setting that was never changed is not in the registry and counts as its default (FIFO buffers on, Receive Buffer 14, Transmit Buffer 16). Windows keeps the registry keys of boxes that were connected before, and two boxes can have the same COM port name; Init then reads the key of the connected box (by its USB serial number). When the port's registry key can't be found or read, or the connected box can't be told apart, there is a warning in the log. The values are on the experiment as `radboudbox_fifo_settings`.

**COM port number (Windows).** The port of the buttonbox (both types) must be COM1 to COM9; Init raises an error for COM10 and higher. Change it in the Device Manager (Ports, the COM port, Properties, Port Settings, Advanced, COM Port Number) to a free number below 10.

**Port settings error (Windows).** On Windows, Init lists all port settings of the box in one error: the COM port number and the latency timer for the BITSI 2015, the COM port number and the FIFO buffers for the BITSI 2018. Each setting is marked correct or incorrect, and the error says where to change them in the Device Manager and what to set. For the BITSI 2015 it also asks to set the USB transfer sizes (Receive and Transmit) to 64 bytes; Init doesn't check those yet.

**Triggers.** Send Trigger works on all boxes, in both modes. Its pulse mode sets the value, waits for the pulse time and sets 0, so it also works with the 2014 firmware.

**Send Control** (extended mode only):

| Command | Sends | 2015, fw 2014 | 2015, fw 2015-11-18 | 2015, fw 2018 | 2018 Teensy | Notes |
|---|---|---|---|---|---|---|
| Calibrate Sound / Voice | `C S` / `C V` | yes | not tested | yes | yes | the item waits 1000 ms: be silent |
| Detect Sound / Voice | `D S` / `D V` | yes | not tested | yes | yes | the box sends `S` / `V` once; collect it with Wait Buttons or Get Buttons (allowed response `S` or `V`) |
| Marker Out | `M` value | yes | yes (tested) | yes | yes | the output keeps the value until the next marker |
| Pulse Out | `P` value | no | yes (tested) | yes | yes | value for the pulse time, then 0 (default 100 ms) |
| Pulse Time | `X` ms | no | yes (tested) | yes | yes | pulse time of Pulse Out, 0-255 ms |
| Analog Out 1 / 2 | `Y` / `Z` value | yes | not tested | yes | yes | 0-255 |
| Tone | `T` | yes | not tested | yes | yes | beep of 100 ms |
| Analog In 1-4 | `A 1`-`A 4` | yes | not tested | yes | yes | the value is logged as `analog_in_[item_name]` |
| LEDs Off / Input / Output | `L X` / `L I` / `L O` | Off and Output | Output (tested); Off and Input not tested | yes | no effect | Input: the LEDs show the buttons; Output: the LEDs show the markers |

The 2014 and 2018 columns follow the firmware sources; the 2015-11-18 column is what was tested on a box. Pulse Out and Pulse Time are an error on a box with the 2014 firmware (when its ID string arrived, and it ends with `Ready!`): that firmware doesn't have them.

## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
  
  
## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
