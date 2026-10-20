OpenSesame Plug-in: Radboud Buttonbox
==========

*An OpenSesame plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2022, Bob Rosbag

This plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 
  
  
## About

The Technical Support Group (Radboud University, Social Sciences) developed an USB Arduino based Buttonbox which can be used for time accurate (1ms) button press, voice key, sound key registration and sending parallel port like triggers.
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

| | BITSI 2015 | BITSI 2018 (Duemilanove) | BITSI 2018 (Teensy 3.6) |
|---|---|---|---|
| Board | Arduino Duemilanove, FTDI USB (0403:6001) | Arduino Duemilanove, FTDI USB (0403:6001) | Teensy 3.6 (USB vendor 16C0) |
| Port on Linux | /dev/ttyUSB*, /dev/serial/by-id/usb-FTDI_* | /dev/ttyUSB*, /dev/serial/by-id/usb-FTDI_* | /dev/ttyACM* |
| ID string (extended mode) | `BITSI_extend mode, Ready!` | `BITSI_extend mode, Ready! w:2018` | `BITSI_extend mode, Ready! w:2018` |
| Simple mode | hold A+H while connecting | hold A+H while connecting | hold A+E while connecting |
| Extended mode | hold B+H while connecting | hold B+H while connecting | hold B+E while connecting |

**Mode.** The box stores its mode (simple or extended) itself. *Bitsi Extended Mode* in the Init item must match it: a box in the other mode sends wrong triggers. Init checks this with the ID string the box sends when it starts, and raises an error when the modes differ. When the ID string doesn't arrive in time, the mode can't be checked; there is a warning in the log.

**Port.** With port *autodetect*, Init takes the first buttonbox it finds (an FTDI, Arduino or Teensy USB device). Other USB serial devices, such as the serial port of an audio interface, are skipped. A *Device id* takes that position in the list of USB serial devices (0 is the device connected last). To choose a port yourself, set *Port*, e.g. `/dev/ttyUSB0` or `COM3`.

**Triggers.** Send Trigger works on all boxes, in both modes. Its pulse mode sets the value, waits for the pulse time and sets 0, so it also works on the BITSI 2015.

**Send Control** (extended mode only):

| Command | Sends | 2015 | 2018 Duemilanove | 2018 Teensy | Notes |
|---|---|---|---|---|---|
| Calibrate Sound / Voice | `C S` / `C V` | yes | yes | yes | the item waits 1000 ms: be silent |
| Detect Sound / Voice | `D S` / `D V` | yes | yes | yes | the box sends `S` / `V` once; collect it with Wait Buttons or Get Buttons (allowed response `S` or `V`) |
| Marker Out | `M` value | yes | yes | yes | the output keeps the value until the next marker |
| Pulse Out | `P` value | no | yes | yes | value for the pulse time, then 0 (default 100 ms) |
| Pulse Time | `X` ms | no | yes | yes | pulse time of Pulse Out, 0-255 ms |
| Analog Out 1 / 2 | `Y` / `Z` value | yes | yes | yes | 0-255 |
| Tone | `T` | yes | yes | yes | beep of 100 ms |
| Analog In 1-4 | `A 1`-`A 4` | yes | yes | yes | the value is logged as `analog_in_[item_name]` |
| LEDs Off / Input / Output | `L X` / `L I` / `L O` | Off and Output | yes | no effect | Input: the LEDs show the buttons; Output: the LEDs show the markers |

Pulse Out and Pulse Time are an error on a BITSI 2015 (when its ID string arrived): its firmware doesn't have them.


## License

This software is distributed under the terms of the GNU General Public License 3. The full license should be included in the file `COPYING`, or can be obtained from:

- <http://www.gnu.org/licenses/gpl.txt>
  
  
## Documentation

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
