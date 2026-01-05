#!/usr/bin/env python3
"""
Button Mapping Tester
Tests and displays all button inputs from the VITURE x 8BitDo controller
using the same mapping logic as controller_bridge.py
"""

import sys
import time

def parse_hat_switch(hat_value):
    """
    Parse HID hat switch value to D-pad directions
    Returns tuple of (up, down, left, right) boolean values
    
    Hat switch values:
    0 = Up
    1 = Up-Right
    2 = Right
    3 = Down-Right
    4 = Down
    5 = Down-Left
    6 = Left
    7 = Up-Left
    8-15 (0x08-0x0F) = Center/None
    """
    if hat_value >= 8:
        return (False, False, False, False)
    
    directions = [
        (True, False, False, False),   # 0: Up
        (True, False, False, True),    # 1: Up-Right
        (False, False, False, True),   # 2: Right
        (False, True, False, True),    # 3: Down-Right
        (False, True, False, False),   # 4: Down
        (False, True, True, False),    # 5: Down-Left
        (False, False, True, False),   # 6: Left
        (True, False, True, False),    # 7: Up-Left
    ]
    
    return directions[hat_value] if hat_value < 8 else (False, False, False, False)

def test_button_mapping():
    try:
        import hid
    except ImportError:
        print("Error: 'hid' package not installed")
        print("Install it with: pip install hid")
        return

    TARGET_VID = 0x2DC8
    TARGET_PID = 0x301F

    print("=" * 70)
    print("VITURE x 8BitDo Controller - Button Mapping Tester")
    print("=" * 70)
    print(f"Looking for controller (VID: 0x{TARGET_VID:04x}, PID: 0x{TARGET_PID:04x})...")
    
    # Find the device
    target_device = None
    for device in hid.enumerate():
        if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
            if device['usage_page'] == 1 and device['usage'] == 5:
                target_device = device
                break
    
    if not target_device:
        # Fallback
        for device in hid.enumerate():
            if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
                target_device = device
                break
    
    if not target_device:
        print("[X] Controller not found!")
        print("\nMake sure:")
        print("  - Controller is plugged in via USB")
        print("  - Controller is in normal mode (not firmware update mode)")
        return

    print(f"[OK] Controller found: {target_device.get('product_string', 'Unknown')}")
    print(f"   Path: {target_device['path']}")
    print("\n" + "=" * 70)
    print("Press buttons on your controller to test them.")
    print("Press Ctrl+C to stop.")
    print("=" * 70)
    print()

    try:
        h = hid.device()
        h.open_path(target_device['path'])
        h.set_nonblocking(1)
        
        last_data = None
        
        while True:
            data = h.read(64)
            if data and len(data) >= 8:
                # Only update display if data changed
                if data != last_data:
                    last_data = data
                    
                    # Parse using same logic as controller_bridge.py
                    b1 = data[1]  # Button Byte 1
                    b2 = data[2]  # Button Byte 2
                    hat = data[3] # D-Pad Hat Switch
                    
                    # Clear screen (Windows compatible)
                    sys.stdout.write("\033[H\033[J")
                    
                    print("=" * 70)
                    print("BUTTON MAPPING TEST - Live Input Display")
                    print("=" * 70)
                    print()
                    
                    # Raw Data
                    print("Raw Data (first 10 bytes):")
                    hex_str = " ".join([f"{b:02x}" for b in data[:10]])
                    print(f"  {hex_str}")
                    print(f"  Byte 1: {b1:02x} ({b1:08b})")
                    print(f"  Byte 2: {b2:02x} ({b2:08b})")
                    print(f"  Hat:    {hat:02x} ({hat:08b})")
                    print()
                    
                    # Buttons from Byte 1
                    print("Buttons from Byte 1:")
                    buttons_1 = []
                    button_map_1 = [
                        (0x01, "A", "XUSB_GAMEPAD_A"),
                        (0x02, "B", "XUSB_GAMEPAD_B"),
                        (0x04, "X", "XUSB_GAMEPAD_X"),
                        (0x08, "Y", "XUSB_GAMEPAD_Y"),
                        (0x10, "LB (L1)", "XUSB_GAMEPAD_LEFT_SHOULDER"),
                        (0x20, "RB (R1)", "XUSB_GAMEPAD_RIGHT_SHOULDER"),
                        (0x40, "L2", "Left Trigger"),
                        (0x80, "R2", "Right Trigger"),
                    ]
                    
                    for mask, name, xbox_name in button_map_1:
                        if b1 & mask:
                            buttons_1.append(f"[*] {name:12s} -> {xbox_name}")
                        else:
                            buttons_1.append(f"[ ] {name:12s}")
                    
                    for btn in buttons_1:
                        print(f"  {btn}")
                    print()
                    
                    # Buttons from Byte 2
                    print("Buttons from Byte 2:")
                    buttons_2 = []
                    button_map_2 = [
                        (0x01, "Select", "XUSB_GAMEPAD_BACK"),
                        (0x02, "Start", "XUSB_GAMEPAD_START"),
                        (0x04, "Home", "XUSB_GAMEPAD_GUIDE"),
                        (0x08, "LS Click", "XUSB_GAMEPAD_LEFT_THUMB"),
                        (0x10, "RS Click", "XUSB_GAMEPAD_RIGHT_THUMB"),
                        (0x20, "Rear 1?", "Not mapped"),
                        (0x40, "Rear 2?", "Not mapped"),
                        (0x80, "Reserved?", "Not mapped"),
                    ]
                    
                    for mask, name, xbox_name in button_map_2:
                        if b2 & mask:
                            buttons_2.append(f"[*] {name:12s} -> {xbox_name}")
                        else:
                            buttons_2.append(f"[ ] {name:12s}")
                    
                    for btn in buttons_2:
                        print(f"  {btn}")
                    print()
                    
                    # D-Pad from Hat Switch
                    print("D-Pad (Hat Switch):")
                    d_up, d_down, d_left, d_right = parse_hat_switch(hat)
                    
                    hat_names = [
                        (d_up, "Up", "XUSB_GAMEPAD_DPAD_UP"),
                        (d_down, "Down", "XUSB_GAMEPAD_DPAD_DOWN"),
                        (d_left, "Left", "XUSB_GAMEPAD_DPAD_LEFT"),
                        (d_right, "Right", "XUSB_GAMEPAD_DPAD_RIGHT"),
                    ]
                    
                    hat_display = []
                    for pressed, name, xbox_name in hat_names:
                        if pressed:
                            hat_display.append(f"[*] {name:12s} -> {xbox_name}")
                        else:
                            hat_display.append(f"[ ] {name:12s}")
                    
                    for hat_btn in hat_display:
                        print(f"  {hat_btn}")
                    print(f"  Hat Value: {hat:02x} ({hat})")
                    
                    # Joystick positions
                    print()
                    print("Joystick Positions:")
                    lx, ly = data[4], data[5]
                    rx, ry = data[6], data[7]
                    print(f"  Left Stick:  X={lx:3d} ({lx:08b}), Y={ly:3d} ({ly:08b})")
                    print(f"  Right Stick: X={rx:3d} ({rx:08b}), Y={ry:3d} ({ry:08b})")
                    
                    # Summary of pressed buttons
                    active_buttons = []
                    if b1 & 0x01: active_buttons.append("A")
                    if b1 & 0x02: active_buttons.append("B")
                    if b1 & 0x04: active_buttons.append("X")
                    if b1 & 0x08: active_buttons.append("Y")
                    if b1 & 0x10: active_buttons.append("LB")
                    if b1 & 0x20: active_buttons.append("RB")
                    if b1 & 0x40: active_buttons.append("L2")
                    if b1 & 0x80: active_buttons.append("R2")
                    if b2 & 0x01: active_buttons.append("Select")
                    if b2 & 0x02: active_buttons.append("Start")
                    if b2 & 0x04: active_buttons.append("Home")
                    if b2 & 0x08: active_buttons.append("LS")
                    if b2 & 0x10: active_buttons.append("RS")
                    if d_up: active_buttons.append("D-Up")
                    if d_down: active_buttons.append("D-Down")
                    if d_left: active_buttons.append("D-Left")
                    if d_right: active_buttons.append("D-Right")
                    
                    print()
                    print("=" * 70)
                    if active_buttons:
                        print(f"ACTIVE: {', '.join(active_buttons)}")
                    else:
                        print("No buttons pressed")
                    print("=" * 70)
            
            time.sleep(0.01)  # Small delay to avoid excessive CPU usage

    except KeyboardInterrupt:
        print("\n\nStopping test...")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            h.close()
        except:
            pass

if __name__ == "__main__":
    test_button_mapping()

