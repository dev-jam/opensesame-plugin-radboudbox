#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Bob Rosbag
2022

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
import os
from setuptools import setup


def get_readme():

    if os.path.exists('README.md'):
        with open('README.md') as fd:
            return fd.read()
    return 'No readme information'


setup(
    name='opensesame-plugin-radboudbox',
    version='2.4.0',
    description='An OpenSesame Plug-in for collecting button responses, audio detection, voice key and sending stimulus synchronization triggers with the Radboud Buttonbox to data acquisition systems.',
    long_description=get_readme(),
    long_description_content_type='text/markdown',
    author='Bob Rosbag',
    author_email='debian@bobrosbag.nl',
    url='https://github.com/dev-jam/opensesame-plugin-radboudbox',
    # Classifiers used by PyPi if you upload the plugin there
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    packages=[],
    data_files=[
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
        [
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.md',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.png',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait_large.png',
            'opensesame_plugins/radboudbox_get_buttons_wait/radboudbox_get_buttons_wait.py',
            'opensesame_plugins/radboudbox_get_buttons_wait/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_init',
        [
            'opensesame_plugins/radboudbox_init/radboudbox_init.md',
            'opensesame_plugins/radboudbox_init/radboudbox_init.png',
            'opensesame_plugins/radboudbox_init/radboudbox_init_large.png',
            'opensesame_plugins/radboudbox_init/radboudbox_init.py',
            'opensesame_plugins/radboudbox_init/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_send_control',
        [
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.md',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.png',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control_large.png',
            'opensesame_plugins/radboudbox_send_control/radboudbox_send_control.py',
            'opensesame_plugins/radboudbox_send_control/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_send_trigger',
        [
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.md',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.png',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger_large.png',
            'opensesame_plugins/radboudbox_send_trigger/radboudbox_send_trigger.py',
            'opensesame_plugins/radboudbox_send_trigger/info.yaml',
            ]
        ),
        ('share/opensesame_plugins/radboudbox_wait_buttons',
        [
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.md',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.png',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons_large.png',
            'opensesame_plugins/radboudbox_wait_buttons/radboudbox_wait_buttons.py',
            'opensesame_plugins/radboudbox_wait_buttons/info.yaml',
            ]
        )]
    )
