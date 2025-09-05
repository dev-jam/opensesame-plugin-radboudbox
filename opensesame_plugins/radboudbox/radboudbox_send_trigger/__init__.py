"""Radboud Buttonbox - sends a trigger"""

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "value",
        "label": "Value",
        "name": "line_edit_value",
        "tooltip": "Value"
    }, {
        "type": "checkbox",
        "var": "pulse_mode",
        "label": "Enable Pulse Mode",
        "name": "checkbox_pulse_mode",
        "tooltip": "Pulse mode"
    }, {
        "type": "line_edit",
        "var": "pulse_time",
        "label": "Pulse Time (ms)",
        "name": "line_edit_pulse_time",
        "tooltip": "Pulse Time (ms)"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": "<small>Radboud Buttonbox version 4.4.0</small>"
    }
]
