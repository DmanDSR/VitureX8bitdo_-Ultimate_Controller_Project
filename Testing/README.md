# Testing Scripts

Scripts for testing and verifying controller button inputs and mappings.

## Files

- **test_buttons_simple.py** - Simple button tester showing which buttons are pressed
- **test_button_mapping.py** - Detailed button mapping tester with Xbox button names
- **test_button_diagnostic.py** - Diagnostic tool showing raw byte values for button mapping
- **test_controller_input.py** - Basic raw HID data logger
- **visualize_controller.py** - Live joystick and button visualizer with ASCII art

## Usage

For quick button testing:
```bash
python test_buttons_simple.py
```

For diagnostic/raw data:
```bash
python test_button_diagnostic.py
```

## Purpose

These scripts help:
- Verify button mappings
- Debug input issues
- Find correct byte positions for buttons
- Test controller functionality

