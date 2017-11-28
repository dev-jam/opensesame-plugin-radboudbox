#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
Author: Bob Rosbag
2017

This plug-in is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this plug-in.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

setup(
    # Some general metadata. By convention, a plugin is named:
    # opensesame-plugin-[plugin name]
    name='opensesame_plugin_-_radboudbox',
    version='1.0.1',
    description='An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.',
    author='Bob Rosbag',
    author_email='b.rosbag@let.ru.nl',
    url='https://github.com/dev-jam/opensesame_plugin_-_radboudbox',
    # Classifiers used by PyPi if you upload the plugin there
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    # The important bit that specifies how the plugin files should be installed,
    # so that they are found by OpenSesame. This is a bit different from normal
    # Python modules, because an OpenSesame plugin is not a (normal) Python
    # module.
    data_files=[
        # First the target folder.
        ('share/opensesame_plugins/radboudbox_get_buttons_start',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_get_buttons_start/radboudbox_get_buttons_start.md',
            'opensesame_plugins/radboudbox_get_buttons_start/radboudbox_get_buttons_start.png',
            'opensesame_plugins/radboudbox_get_buttons_start/radboudbox_get_buttons_start_large.png',
            'opensesame_plugins/radboudbox_get_buttons_start/radboudbox_get_buttons_start.py',
            'opensesame_plugins/radboudbox_get_buttons_start/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_get_buttons_wait',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.md',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.png',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait_large.png',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.py',
            'opensesame_plugins/radboudbox_get_buttons_wait/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_init',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_init/radboudbox_init.md',
            'opensesame_plugins/radboudbox_init/radboudbox_init.png',
            'opensesame_plugins/radboudbox_init/radboudbox_init_large.png',
            'opensesame_plugins/radboudbox_init/radboudbox_init.py',
            'opensesame_plugins/radboudbox_init/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_send_control',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.md',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.png',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control_large.png',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.py',
            'opensesame_plugins/radboudbox_send_control/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_send_trigger',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.md',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.png',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger_large.png',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.py',
            'opensesame_plugins/radboudbox_send_trigger/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_wait_buttons',
        # Then a list of files that are copied into the target folder. Make sure
        # that these files are also included by MANIFEST.in!
        [
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.md',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.png',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons_large.png',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.py',
            'opensesame_plugins/radboudbox_wait_buttons/info.yaml',
            ]
        )]
    )
