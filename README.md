<<<<<<< HEAD
# VITURE x 8BitDo Controller - PC Driver & Reverse Engineering

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**Unlock Xbox 360 compatibility/X-Input for the VITURE x 8BitDo Ultimate Mobile Gaming Controller.**

</div>

## 📖 The Problem
The [VITURE x 8BitDo Ultimate Mobile Gaming Controller](https://www.viture.com/store) is a premium controller designed for Android. However, out of the box, it lacks proper PC compatibility modes:
-   **No X-Input (Xbox Mode):** Games from Game Pass, Epic, etc., do not recognize it.
-   **No Switch/Mac Mode:** Hardware switching combos (`X+Start`, etc.) are disabled in the firmware (`VID: 0x2DC8`, `PID: 0x301F`).
-   **No iOS Support:** Lacks the MFi certification or X-Input required for iPhone.

## 🛠️ The Solution: Virtual Bridge
Since the firmware is locked, I built a **Software Bridge** that sits between the controller and Windows. It reads the raw HID input and feeds it into a "Virtual Xbox 360 Controller" driver.

**Result:** Windows thinks an official Xbox 360 controller is plugged in. Works with all PC games, Steam, and Emulators.

---

## 🚀 Quick Start (For Users)

### Prerequisites
You must install the **ViGEmBus Driver** (Virtual Gamepad Emulation Bus) for this to work.
-   [Download ViGEmBus Installer](https://github.com/ViGEm/ViGEmBus/releases/latest)

### Usage
1.  **Download** the latest release (`VITURE_Controller_Bridge.exe`) from the [dist/](dist/) folder.
2.  **Plug in** your VITURE controller via USB.
3.  **Run** `VITURE_Controller_Bridge.exe`.
4.  Leave the window open while gaming. You will see a "Connected" message.

---

## 🧑‍💻 Developer Guide (Running from Source)

If you want to modify the mapping or sensitivity:

1.  **Install Dependencies:**
    ```bash
    pip install vgamepad hidapi
    ```
2.  **Run the script:**
    ```bash
    python bridge/controller_bridge.py
    ```

### Building the Exe
To compile the script into a standalone executable yourself:
```bash
pip install pyinstaller
pyinstaller --onefile --name "VITURE_Controller_Bridge" bridge/controller_bridge.py
```

---

## 🔬 Reverse Engineering Findings

For those interested in the hardware hacking journey, check out the [Controller_Hack_Findings](Controller_Hack_Findings/) folder.

### Key Discoveries
-   **Default Mode:** `VID: 2DC8` | `PID: 301F` (Android D-Input)
-   **Hidden Update Mode:** `VID: 2DC8` | `PID: 3208` (Access by holding `L1+R1` while plugging in)
-   **Firmware Tools:** 8BitDo's `dfu4.exe` is present but encrypted/silent.
-   **Hardware Locks:** Physical mode switching (X/Y/A + Start) is disabled in this specific OEM firmware.

### Included Tools
This repo includes Python scripts organized by function:

**Bridge Scripts** (`bridge/`):
-   `controller_bridge.py` - Main bridge that converts controller input to Xbox 360 format

**Testing Scripts** (`testing/`):
-   `test_buttons_simple.py` - Simple button tester
-   `test_button_diagnostic.py` - Diagnostic tool for button mapping
-   `visualize_controller.py` - Live ASCII art visualizer for joystick/button testing

**Analysis Scripts** (`analysis/`):
-   `detect_usb_devices.py` - Scans USB bus for PID changes (useful for finding hidden modes)
-   `hid_device_inspector.py` - Dumps HID Report Descriptors
-   `check_device_storage.py` - Checks for accessible firmware storage

---

## ⚠️ Disclaimer
This project is an unofficial community modification and is not affiliated with VITURE or 8BitDo. Use at your own risk.
=======
# VITURE x 8BitDo Controller - PC Driver & Reverse Engineering

<div align="center">

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

**Unlock Xbox 360 compatibility/X-Input for the VITURE x 8BitDo Ultimate Mobile Gaming Controller.**

</div>

## 📖 The Problem
The [VITURE x 8BitDo Ultimate Mobile Gaming Controller](https://www.viture.com/store) is a premium controller designed for Android. However, out of the box, it lacks proper PC compatibility modes:
-   **No X-Input (Xbox Mode):** Games from Game Pass, Epic, etc., do not recognize it.
-   **No Switch/Mac Mode:** Hardware switching combos (`X+Start`, etc.) are disabled in the firmware (`VID: 0x2DC8`, `PID: 0x301F`).
-   **No iOS Support:** Lacks the MFi certification or X-Input required for iPhone.

## 🛠️ The Solution: Virtual Bridge
Since the firmware is locked, I built a **Software Bridge** that sits between the controller and Windows. It reads the raw HID input and feeds it into a "Virtual Xbox 360 Controller" driver.

**Result:** Windows thinks an official Xbox 360 controller is plugged in. Works with all PC games, Steam, and Emulators.

---

## 🚀 Quick Start (For Users)

### Prerequisites
You must install the **ViGEmBus Driver** (Virtual Gamepad Emulation Bus) for this to work.
-   [Download ViGEmBus Installer](https://github.com/ViGEm/ViGEmBus/releases/latest)

### Usage
1.  **Download** the latest release (`VITURE_Controller_Bridge.exe`) from the [dist/](dist/) folder.
2.  **Plug in** your VITURE controller via USB.
3.  **Run** `VITURE_Controller_Bridge.exe`.
4.  Leave the window open while gaming. You will see a "Connected" message.

---

## 🧑‍💻 Developer Guide (Running from Source)

If you want to modify the mapping or sensitivity:

1.  **Install Dependencies:**
    ```bash
    pip install vgamepad hidapi
    ```
2.  **Run the script:**
    ```bash
    python bridge/controller_bridge.py
    ```

### Building the Exe
To compile the script into a standalone executable yourself:
```bash
pip install pyinstaller
pyinstaller --onefile --name "VITURE_Controller_Bridge" bridge/controller_bridge.py
```

---

## 🔬 Reverse Engineering Findings

For those interested in the hardware hacking journey, check out the [Controller_Hack_Findings](Controller_Hack_Findings/) folder.

### Key Discoveries
-   **Default Mode:** `VID: 2DC8` | `PID: 301F` (Android D-Input)
-   **Hidden Update Mode:** `VID: 2DC8` | `PID: 3208` (Access by holding `L1+R1` while plugging in)
-   **Firmware Tools:** 8BitDo's `dfu4.exe` is present but encrypted/silent.
-   **Hardware Locks:** Physical mode switching (X/Y/A + Start) is disabled in this specific OEM firmware.

### Included Tools
This repo includes Python scripts organized by function:

**Bridge Scripts** (`bridge/`):
-   `controller_bridge.py` - Main bridge that converts controller input to Xbox 360 format

**Testing Scripts** (`testing/`):
-   `test_buttons_simple.py` - Simple button tester
-   `test_button_diagnostic.py` - Diagnostic tool for button mapping
-   `visualize_controller.py` - Live ASCII art visualizer for joystick/button testing

**Analysis Scripts** (`analysis/`):
-   `detect_usb_devices.py` - Scans USB bus for PID changes (useful for finding hidden modes)
-   `hid_device_inspector.py` - Dumps HID Report Descriptors
-   `check_device_storage.py` - Checks for accessible firmware storage

---

## ⚠️ Disclaimer
This project is an unofficial community modification and is not affiliated with VITURE or 8BitDo. Use at your own risk.
>>>>>>> 98d193724cd3ec1bfca0d21e059c3a30b2c9dd50
