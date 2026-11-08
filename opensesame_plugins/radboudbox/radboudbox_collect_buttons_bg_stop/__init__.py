# Copyright (C) 2016-2026 Bob Rosbag <mail@bobrosbag.nl>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Radboud Buttonbox - stops the background button registration"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "text",
        "label": "Ends the button registration of the background item, also when it has no timeout. The responses until then are logged."
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": f"<small>Radboud Buttonbox version {__version__}</small>"
    }
]
