OpenSesame Plug-in: Radboud Buttonbox plugin
==========

*An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2017, Bob Rosbag  

This plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 
  
  
## 1. About
--------

The Technical Support Group (Radboud University, Social Sciences) developed an USB Arduino based Buttonbox which can be used for time accurate(1ms) button press, voice key, sound key registration and sending parallel port like triggers.
Upper case A, B, C, D, E, F are used for key presses, and lower case a, b, c, d, e, f are used for key releases. Uppercase S is used for sound key detection and uppercase V for voice key.  

For more information:

<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>


This plug-in consist of foreground and background (multithreaded) items.


Difference between foreground and background:

- **Foreground** item starts button/signal registration until it detects an allowed button or the set duration has passed. 
- **Background** item consist of a 'start' and 'wait' item. These are fully multi-threaded. After the start of the button/signal registration, the item will immediately advance to the next item. When the experiment reaches the 'wait' item, it will wait until a button/signal has been detected by the 'start' item or the duration has passed.


This plug-in has six items:

- **Init** initialization of the buttonbox, this should be placed at the beginning of an experiment.
- **Wait Buttons** waits for a button press or release before continuing to the next item in the experiment
- **Get Buttons Start** starts a new thread which monitors for button presses/releases, it will directly advance to the next item in the experiment
- **Get buttons Wait** waits until the thread from 'Get Buttons Start' is finished (has detected a button press/release) before advancing to the next item in the experiment 
- **Send Control** send control code to the buttonbox, for example 'Calibrate Sound', 'Detect Sound'
- **Send Trigger** for sending triggers to hardware with a parallel port


Timestamps can be found in the logs by the name: time_response_[item_name]


Linux, and Windows are supported (possible also OSX, not tested). The plug-in will first look for the globally installed rusocsci package. If this is not available, the shipped version will be used. Install options are listed below.
  
  
## 2. LICENSE
----------

The Radboud Buttonbox plug-in is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others. For the full license information, please
refer to `debian/copyright`.
  
  
## 3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
