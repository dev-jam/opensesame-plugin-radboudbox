"""Radboud Buttonbox - initializes the buttonbox"""

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "checkbox",
        "var": "dummy_mode",
        "label": "Dummy Mode",
        "name": "checkbox_dummy",
        "tooltip": "Run in dummy mode"
    }, {
        "type": "checkbox",
        "var": "verbose",
        "label": "Verbose Mode",
        "name": "checkbox_verbose",
        "tooltip": "Run in verbose mode"
    }, {
        "type": "line_edit",
        "var": "id",
        "label": "Device id",
        "name": "line_edit_id",
        "tooltip": "Expecting a valid device name or autodetect."
    }, {
        "type": "line_edit",
        "var": "port",
        "label": "Port",
        "name": "line_edit_port",
        "tooltip": "Expecting a valid port device name or autodetect."
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": "<small>Radboud Buttonbox version 3.1.0</small>"
    }
]