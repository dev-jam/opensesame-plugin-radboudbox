OpenSesame Plug-in: Radboud Buttonbox 'Init' plugin
==========

*An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2020, Bob Rosbag  

This plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 


## 1. About
--------

The Technical Support Group (Radboud University, Social Sciences) developed an USB Arduino based Buttonbox which can be used for time accurate(1ms) button press, voice key, sound key registration and sending parallel port like triggers.
Upper case A, B, C, D, E, F are used for key presses, and lower case a, b, c, d, e, f are used for key releases. Uppercase S is used for sound key detection and uppercase V for voice key.  

This plug-in has four items:

- *Dummy mode* for testing experiments.
- *Verbose mode* for testing experiments.
- *Device ID* a valid device name. Leave empty for autodetect.
- *Port* a valid port device name. Leave empty for autodetect.

Linux, and Windows are supported (possible also OSX, not tested). The plug-in will first look for the globally installed rusocsci package. If this is not available, the shipped version will be used. Install options are listed below.


For more information:

<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>



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
