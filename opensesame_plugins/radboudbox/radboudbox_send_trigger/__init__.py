"""Radboud Buttonbox - sends a trigger"""

from .. import __version__

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "value",
        "label": "Value",
        "name": "line_edit_value",
        "info": "0-255"
    }, {
        "type": "checkbox",
        "var": "pulse_mode",
        "label": "Enable Pulse Mode",
        "name": "checkbox_pulse_mode"
    }, {
        "type": "line_edit",
        "var": "pulse_time",
        "label": "Pulse Time (ms)",
        "name": "line_edit_pulse_time"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": f"<small>Radboud Buttonbox version {__version__}</small>"
    }
]
