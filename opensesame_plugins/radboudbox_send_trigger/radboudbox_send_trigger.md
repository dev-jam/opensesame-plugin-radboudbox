OpenSesame Plug-in: Radboud Buttonbox 'Send Trigger' plugin
==========

*An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.*  

Copyright, 2020, Bob Rosbag  

This plugin makes use of the RuSocSci python package developed by Wilbert van der Ham. Radboud Buttonbox is developed by Pascal de Water. Exact references will follow in the future. 

## 1. About
--------

In EEG/ERP studies it is common to send triggers to mark timestamp for significant events (e.g., the onset of a trial, presentation of a particular stimulus, etc.). Triggers are typically bytes that are sent via the parallel port to data acquisition systems.
The Technical Support Group (Radboud University, Social Sciences) developed an USB Arduino based Buttonbox which can send low latency parallel port like triggers without the use of an actual parallel port.  

This plug-in has three options:

- *Value* is a positive integer between 1-255 and specifies the trigger byte


For more information:

<http://tsgdoc.socsci.ru.nl/index.php?title=ButtonBoxes>


## 2. LICENSE
----------

The Radboud Buttonbox 'Send Trigger' plug-in is distributed under the terms of the GNU General Public License 3.
The full license should be included in the file COPYING, or can be obtained from

- <http://www.gnu.org/licenses/gpl.txt>

This plug-in contains works of others. For the full license information, please
refer to `debian/copyright`.


## 3. Documentation
----------------

Installation instructions and documentation on OpenSesame are available on the documentation website:

- <http://osdoc.cogsci.nl/>
