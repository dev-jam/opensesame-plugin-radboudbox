# Copyright (C) 2016-2026 Bob Rosbag <mail@bobrosbag.nl>
# SPDX-License-Identifier: GPL-3.0-or-later

"""Radboud Buttonbox - starts button registration in the background"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# The item type of this item in experiments made before 6.0.0
aliases = ["radboudbox_get_buttons_start"]
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses",
        "name": "line_edit_allowed_responses",
        "info": "e.g. A;B (a-h release, S/V sound/voice)"
    }, {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response",
        "name": "line_edit_correct_response",
        "info": "e.g. A, or A;B"
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout (ms)",
        "name": "line_edit_timeout",
        "info": "In ms, or 'infinite'"
    }, {
        "type": "line_edit",
        "var": "number_of_responses",
        "label": "Number of responses (1 or more, or infinite)",
        "name": "line_edit_number_of_responses",
        "info": "infinite: all until the timeout"
    }, {
        "type": "text",
        "label": "<b>IMPORTANT:</b> this is a multithreaded background item, it will immediately advance to the next item, it will NOT wait for the button press/release or till the timeout has ended."
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": f"<small>Radboud Buttonbox version {__version__}</small>"
    }
]
