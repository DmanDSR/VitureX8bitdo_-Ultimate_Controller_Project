# Analysis Scripts

Scripts for device detection, reverse engineering, and firmware analysis.

## Files

- **detect_usb_devices.py** - Scans USB bus to find the controller and detect mode changes
- **hid_device_inspector.py** - Dumps HID report descriptors and device information
- **check_device_storage.py** - Checks if controller appears as storage device (for firmware files)
- **inspect_controller_pyusb.py** - Controller inspection using pyusb library
- **inspect_new_mode.py** - Inspects the firmware update mode (L1+R1 while plugging)
- **analyze_8bitdo_software.py** - Analyzes the official 8BitDo software

## Usage

To find your controller:
```bash
python detect_usb_devices.py
```

To inspect HID capabilities:
```bash
python hid_device_inspector.py
```

## Purpose

These scripts help:
- Identify controller device IDs and modes
- Understand HID protocol structure
- Find firmware update modes
- Reverse engineer controller behavior

