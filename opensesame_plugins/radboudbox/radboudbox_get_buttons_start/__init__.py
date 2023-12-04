"""Radboud Buttonbox - starts button registration in the background"""

# The category determines the group for the plugin in the item toolbar
category = "RadboudBox"
# Defines the GUI controls
controls = [
    {
        "type": "line_edit",
        "var": "allowed_responses",
        "label": "Allowed responses",
        "name": "line_edit_allowed_responses",
        "tooltip": "Expecting a semicolon-separated list of button characters, e.g., A;B;C - Upper-case (H) for presses, lower-case (h) for release and S / V for sound/voice detect etc..."
    }, {
        "type": "line_edit",
        "var": "correct_response",
        "label": "Correct response",
        "name": "line_edit_correct_response",
        "tooltip": "Expecting a semicolon-separated list of button characters, e.g., A;B;C - Upper-case (H) for presses, lower-case (h) for release and S / V for sound/voice detect etc..."
    }, {
        "type": "line_edit",
        "var": "timeout",
        "label": "Timeout (ms)",
        "name": "line_edit_timeout",
        "tooltip": "Expecting a value in milliseconds or 'infinite'"
    }, {
        "type": "text",
        "label": "<b>IMPORTANT:</b> this is a multithreaded background item, it will immediately advance to the next item, it will NOT wait for the button press/release or till the timeout has ended."
    }, {
        "type": "text",
        "label": "<small><b>Note:</b> Radboudbox init item at the begin of the experiment is needed for initialization of the buttonbox</small>"
    }, {
        "type": "text",
        "label": "<small>Radboud Buttonbox version 3.1.0</small>"
    }
]
