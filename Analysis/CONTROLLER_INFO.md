<<<<<<< HEAD
# VITURE x 8BitDo Controller Information

## Device Identifiers

- **Model:** VITURE x 8BitDo Ultimate Mobile Gaming Controller
- **Vendor ID (VID):** `0x2DC8` (11720 decimal)
- **Product ID (PID):** `0x301F` (12319 decimal)
- **Device Instance ID Pattern:** `USB\VID_2DC8&PID_301F\...`

## Windows Detection

From Windows Event Viewer and Device Manager:
- Appears as: **USB Composite Device**
- Location: `Port_#0004.Hub_#0001`
- Status: "This device is working properly"
- Class GUID: `{36fc9e60-c465-11cf-8056-444553540000}` (USB devices)

## Known Issues

- **Windows Migration Warning:** Event ID 442 - Device settings not migrated from previous OS installation
  - Status Code: `0xC0000719`
  - This is typically harmless and doesn't affect functionality

## Current Compatibility

✅ **Works With:**
- Android 13+ devices (USB-C OTG)
- Windows computers (as gamepad)
- VITURE XR Glasses (Android)
- Computer gamepad testing sites

❌ **Does NOT Work With:**
- iPhone/iOS devices (iOS model "coming soon" but not available)

## Technical Specifications

- **Connection:** USB-C (low-latency, no Bluetooth)
- **Features:**
  - Hall Effect joysticks and triggers
  - Tactile bumpers
  - Refined D-pad
  - Two rear buttons
  - P1 button (mouse control mode)
- **Software:** 8BitDo Ultimate Software V2 (button mapping/customization)
- **Dimensions:** 197.22 x 102.66 x 53.48 mm
- **Weight:** 244.5 g

## USB-C Ports

- **USB-C1 (Android Phones):** Input 5V/1A; Output 5V/2A, 9V/3A, 12V/3A, 15V/3A
- **USB-C2 (Chargers):** Input 5V/2A, 9V/3A, 12V/3A, 15V/3A
- **USB-C3 (XR Glasses):** Supports video transmission; Output 5V/1A; USB 2.0 data transfer

## Detection Scripts

The following scripts have been enhanced to specifically detect this controller:

1. **detect_usb_devices.py** - Will highlight when this controller is found
2. **hid_device_inspector.py** - Will mark this controller as the target device
3. **check_device_storage.py** - Check for accessible firmware files

## Next Steps for iPhone Compatibility

1. Check if 8BitDo provides firmware update tools
2. Inspect HID report descriptor for platform-specific code
3. Look for firmware files in accessible storage
4. Research if other 8BitDo controllers have iPhone support and compare firmware
5. Check for community firmware modifications

=======
# VITURE x 8BitDo Controller Information

## Device Identifiers

- **Model:** VITURE x 8BitDo Ultimate Mobile Gaming Controller
- **Vendor ID (VID):** `0x2DC8` (11720 decimal)
- **Product ID (PID):** `0x301F` (12319 decimal)
- **Device Instance ID Pattern:** `USB\VID_2DC8&PID_301F\...`

## Windows Detection

From Windows Event Viewer and Device Manager:
- Appears as: **USB Composite Device**
- Location: `Port_#0004.Hub_#0001`
- Status: "This device is working properly"
- Class GUID: `{36fc9e60-c465-11cf-8056-444553540000}` (USB devices)

## Known Issues

- **Windows Migration Warning:** Event ID 442 - Device settings not migrated from previous OS installation
  - Status Code: `0xC0000719`
  - This is typically harmless and doesn't affect functionality

## Current Compatibility

✅ **Works With:**
- Android 13+ devices (USB-C OTG)
- Windows computers (as gamepad)
- VITURE XR Glasses (Android)
- Computer gamepad testing sites

❌ **Does NOT Work With:**
- iPhone/iOS devices (iOS model "coming soon" but not available)

## Technical Specifications

- **Connection:** USB-C (low-latency, no Bluetooth)
- **Features:**
  - Hall Effect joysticks and triggers
  - Tactile bumpers
  - Refined D-pad
  - Two rear buttons
  - P1 button (mouse control mode)
- **Software:** 8BitDo Ultimate Software V2 (button mapping/customization)
- **Dimensions:** 197.22 x 102.66 x 53.48 mm
- **Weight:** 244.5 g

## USB-C Ports

- **USB-C1 (Android Phones):** Input 5V/1A; Output 5V/2A, 9V/3A, 12V/3A, 15V/3A
- **USB-C2 (Chargers):** Input 5V/2A, 9V/3A, 12V/3A, 15V/3A
- **USB-C3 (XR Glasses):** Supports video transmission; Output 5V/1A; USB 2.0 data transfer

## Detection Scripts

The following scripts have been enhanced to specifically detect this controller:

1. **detect_usb_devices.py** - Will highlight when this controller is found
2. **hid_device_inspector.py** - Will mark this controller as the target device
3. **check_device_storage.py** - Check for accessible firmware files

## Next Steps for iPhone Compatibility

1. Check if 8BitDo provides firmware update tools
2. Inspect HID report descriptor for platform-specific code
3. Look for firmware files in accessible storage
4. Research if other 8BitDo controllers have iPhone support and compare firmware
5. Check for community firmware modifications

>>>>>>> 98d193724cd3ec1bfca0d21e059c3a30b2c9dd50
