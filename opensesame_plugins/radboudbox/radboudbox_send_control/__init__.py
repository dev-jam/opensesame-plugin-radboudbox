"""Radboud Buttonbox - sends a control command to the buttonbox"""

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
       "type": "combobox",
       "var": "command",
       "label": "Send Command",
       "options": [
           "Calibrate Sound",
           "Calibrate Voice",
           "Detect Sound",
           "Detect Voice",
           "Marker Out",
           "Pulse Out",
           "Pulse Time",
           "Analog Out 1",
           "Analog Out 2",
           "Tone",
           "Analog In 1",
           "Analog In 2",
           "Analog In 3",
           "Analog In 4",
           "LEDs Off",
           "LEDs Input",
           "LEDs Output"
       ],
       "name": "combobox_command",
       "tooltip": "Send command to the RadboudBox"
    }, {
        "type": "line_edit",
        "var": "command_value",
        "label": "Command Value",
        "name": "line_edit_command_value",
        "tooltip": "Command Value"
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": "<small>Radboud Buttonbox version 3.1.0</small>"
    }
]
