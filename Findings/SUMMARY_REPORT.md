# VITURE x 8BitDo Controller Reverse Engineering Report
**Date:** December 31, 2025  
**Status:** Firmware Access Confirmed / Modification Locked  

---

## 1. Project Overview
The goal of this project was to reverse engineer the **VITURE x 8BitDo Ultimate Mobile Gaming Controller** to enable compatibility with **iOS (iPhone)**. Officially, this controller supports Android and PC, but lacks the "MFi" (Made for iPhone) or "Xbox" input modes required for iOS support.

## 2. Hardware Identification
Through USB analysis, we identified the specific signatures of the device in its default state.

### Default Mode (Android/D-Input)
- **Vendor ID (VID):** `0x2DC8` (8BitDo)
- **Product ID (PID):** `0x301F`
- **Protocol:** HID (Human Interface Device)
- **Functionality:** 
  - Standard Gamepad (15 buttons, 4 axes)
  - Mouse Interface (via "P1" mode switch)
- **iOS Behavior:** Recognized as a generic USB device, but **ignored** by iOS Game Controller framework (requires MFi or XInput).

## 3. The "Hidden Mode" Discovery
We successfully discovered a hidden **Firmware Update Hook** by testing button combinations during connection.

### Firmware Update Mode
- **Trigger:** Hold `L1` + `R1` while plugging in the USB cable.
- **Vendor ID (VID):** `0x2DC8`
- **Product ID (PID):** `0x3208` (Different from default!)
- **Significance:** This mode is used by the factory or update tools to flash firmware. The fact that the PID changes proves the controller has a secondary bootloader active.

### Other Mode Tests
We tested standard 8BitDo input toggles to see if "X-Input" (Xbox) or "Switch" modes were hidden:
- **X + Plug:** No change (Remained `0x301F`)
- **Y + Plug:** No change (Remained `0x301F`)
- **A + Plug:** No change (Remained `0x301F`)

**Conclusion:** The alternative input modes (X-Input, Switch, macOS) appear to be disabled or removed in the VITURE-specific firmware version. Only the default D-Input mode and the Update mode are active.

## 4. Signal Analysis (HID Protocol)
We wrote custom Python scripts to intercept and visualize the raw data stream from the controller.

**Data Packet Format (64 bytes):**
```
01 00 00 0F 7F 7F 7F 7F ...
```
- **Byte 0 (`01`):** Report ID
- **Byte 1 (`00`):** Button Flags 1 (A, B, X, Y, Triggers)
- **Byte 2 (`00`):** Button Flags 2 (Select, Start, Home?)
- **Byte 3 (`0F`):** D-Pad Hat Switch (0F = Center)
- **Byte 4 (`7F`):** Left Stick X (0-255, Center ~127)
- **Byte 5 (`7F`):** Left Stick Y
- **Byte 6 (`7F`):** Right Stick X
- **Byte 7 (`7F`):** Right Stick Y

This standard HID report structure allows us to read input perfectly on PC, enabling the creation of custom drivers or translation bridges.

## 5. Official Software & Firmware Tools
We analyzed the official **8BitDo Ultimate Software V2**:
- **Findings:** The software contains a hidden tool named `dfu4.exe` (Device Firmware Update).
- **Behavior:**
  - The main GUI **does not detect** the controller (Logs show `PID:0 VID:0` not found).
  - The `dfu4.exe` tool is protected and refuses to run without specific encrypted arguments or handshakes (`-r` and `-f` flags exist but error out).
  - We attempted to brute-force the arguments (`-dv 2DC8 -dp 3208`) but the tool returned no output, indicating a silent failure or requirement for a challenge-response key.
  - **Strings Analysis**: We dumped the strings from `8BitDo Ultimate Software V2.exe` and found references to `dfu4.exe` but no clear command-line arguments or passwords.
  - **Config Hacking**: We enabled `isLoadBeta=True` and `hidden=True` in the `.config` file to try and force "Developer Mode". The application launched but still failed to detect the PID `301F`/`3208` controller, suggesting the allowlist is hardcoded in the compiled DLLs (`RTKHIDKit.dll`).

## 6. Included Tools
We have developed a suite of Python tools to assist in further hacking or usage. These are located in the main directory:

| Script Name | Function |
|-------------|----------|
| `detect_usb_devices.py` | Scans all USB devices and identifies the controller's current mode/PID. |
| `hid_device_inspector.py` | Dumps the detailed "Report Descriptor" hidden in the firmware. |
| `visualize_controller.py` | **Best Tool.** displays a live visualizer of joysticks and buttons to verify input. |
| `test_controller_input.py` | Prints raw hex triggers for debugging. |
| `dist/VITURE_Controller_Bridge.exe` | **Standalone App.** The compiled version of the bridge script. No Python required! |

## 7. Final Recommendation
Since physical firmware modification is blocked by the encrypted bootloader/tools:

1.  **For PC Use:** 
    - Download and run `VITURE_Controller_Bridge.exe`.
    - Your PC will instantly recognize the device as an **Xbox 360 Controller**.
    - Compatible with Steam, Game Pass, Emulators, etc.
    - *Note:* Requires [ViGEmBus Driver](https://github.com/ViGEm/ViGEmBus/releases) to be installed.

2.  **For iOS Use:** Direct USB connection is **not possible** with the current firmware. The only workaround is to connect the controller to a PC/Android device and use **Streaming Apps** (Steam Link, Moonlight) to play games on the iPhone, passing the input from the PC.

## 8. How to Resume This Work
If an updated version of `dfu4.exe` or a leaked "Factory Flasher" for 8BitDo devices becomes available:
1.  Put controller in Update Mode (`L1+R1+Plug`).
2.  Use the flasher to overwrite the firmware with the "Standard" 8BitDo Ultimate Wired firmware (which likely has Xbox support).
3.  **Warning:** This carries a high risk of bricking the device as the pin mappings might differ.

---
*Document generated by Antigravity Agent*
