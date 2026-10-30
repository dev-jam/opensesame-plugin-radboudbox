"""Radboud Buttonbox - initializes the buttonbox"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "dummy_mode",
        "label": "Dummy Mode",
        "name": "checkbox_dummy",
        "info": "No buttonbox: keyboard, nothing sent"
    }, {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose Mode",
        "name": "checkbox_verbose",
        "info": "Messages in the debug window"
    }, {
        "type": "line_edit",
        "var": "id",
        "label": "Device id",
        "name": "line_edit_id",
        "info": "autodetect = first buttonbox, 0 = last connected"
    }, {
        "type": "line_edit",
        "var": "port",
        "label": "Port",
        "name": "line_edit_port",
        "info": "e.g. /dev/ttyACM0 or COM3"
    }, {
        "type": "checkbox",
        "var": "extended_mode",
        "label": "Bitsi Extended Mode",
        "name": "checkbox_extended",
        "info": "Must match the mode of the box; needed for Send Control"
    }, {
        "type": "combobox",
        "var": "wrong_port_settings",
        "label": "Wrong port settings",
        "options": [
            "error",
            "warning"
        ],
        "name": "combobox_wrong_port_settings",
        "info": "error: stop; warning: go on, logged"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": f"<small>Radboud Buttonbox version {__version__}</small>"
    }
]
