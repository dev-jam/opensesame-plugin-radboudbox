# Copyright (C) 2016-2026 Bob Rosbag <mail@bobrosbag.nl>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Radboud Buttonbox - waits until the background button registration has finished"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# The item type of this item in experiments made before 6.0.0
aliases = ["radboudbox_get_buttons_wait"]
# Defines the GUI controls
controls = [
    {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": f"<small>Radboud Buttonbox version {__version__}</small>"
    }
]
