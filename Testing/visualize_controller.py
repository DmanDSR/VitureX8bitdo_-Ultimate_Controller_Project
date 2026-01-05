#!/usr/bin/env python3
"""
Controller Joystick Visualizer
Visualizes the joystick and trigger values from the controller in real-time.
"""

import sys
import os
import time
import math

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_bar(value, width=20):
    """Draw a progress bar for a value between 0 and 255"""
    normalized = value / 255.0
    filled = int(normalized * width)
    return "[" + "#" * filled + " " * (width - filled) + f"] {value:3d}"

def draw_joystick(x, y, size=10):
    """Draw a 2D representation of joystick position"""
    # Normalize 0-255 to -1.0 to 1.0 (approximate, center is 127/128)
    norm_x = (x - 128) / 128.0
    norm_y = (y - 128) / 128.0
    
    # Grid size
    grid_x = size * 2 + 1
    grid_y = size + 1
    
    # Calculate position
    pos_x = int((norm_x + 1) * size)
    pos_y = int((norm_y + 1) * (size / 2))
    
    # Clamp to bounds
    pos_x = max(0, min(grid_x - 1, pos_x))
    pos_y = max(0, min(grid_y - 1, pos_y))
    
    output = []
    output.append(f"  X: {x:3d}  Y: {y:3d}")
    output.append("  +" + "-" * grid_x + "+")
    
    for r in range(grid_y):
        line = "  |"
        for c in range(grid_x):
            if r == pos_y and c == pos_x:
                line += "O"
            elif r == size // 2 and c == size:
                line += "+"
            else:
                line += " "
        line += "|"
        output.append(line)
    
    output.append("  +" + "-" * grid_x + "+")
    return "\n".join(output)

def visualize_controller():
    try:
        import hid
    except ImportError:
        print("Error: 'hid' package not installed")
        return

    TARGET_VID = 0x2DC8
    TARGET_PID = 0x301F

    print(f"Looking for controller (VID: 0x{TARGET_VID:04x}, PID: 0x{TARGET_PID:04x})...")
    
    # Find the device
    target_device = None
    for device in hid.enumerate():
        if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
            if device['usage_page'] == 1 and device['usage'] == 5:
                target_device = device
                break
    
    if not target_device:
        print("Controller not found.")
        return

    print("Controller found! Reading input data...")
    time.sleep(1)

    try:
        h = hid.device()
        h.open_path(target_device['path'])
        h.set_nonblocking(1)
        
        print("\n\n")

        while True:
            # Read data
            data = h.read(64)
            if data and len(data) >= 8:
                # Based on previous output: 01 80 00 0f 7f 7f 7f 7f
                # Likely mapping:
                # Byte 0: Report ID? (01)
                # Byte 1: Buttons (A, B, X, Y, LB, RB, etc.)
                # Byte 2: D-Pad / potentially more buttons
                # Byte 3: ?
                # Byte 4: Left Stick X
                # Byte 5: Left Stick Y
                # Byte 6: Right Stick X (mapped to RZ)
                # Byte 7: Right Stick Y (mapped to Z)
                
                # Note: This mapping is a guess and needs verification
                # 8BitDo usually follows standard XInput or Switch Pro mapping patterns
                
                # Check for buttons
                buttons1 = data[1]
                buttons2 = data[2]
                
                lx = data[4]
                ly = data[5]
                rx = data[6]
                ry = data[7]
                
                # Clear and redraw
                # Using ANSI escape codes to move cursor up instead of clearing screen to reduce flicker
                sys.stdout.write("\033[H\033[J") 
                
                print("VITURE x 8BitDo Controller Visualization")
                print("=" * 40)
                print(f"Raw Data: {' '.join([f'{b:02x}' for b in data[:10]])}")
                print("-" * 40)
                
                print(f"Left Analog Stick:")
                print(draw_joystick(lx, ly))
                
                print("\nRight Analog Stick:")
                print(draw_joystick(rx, ry))
                
                print("-" * 40)
                print(f"Buttons 1: {buttons1:08b} (Hex: {buttons1:02x})")
                print(f"Buttons 2: {buttons2:08b} (Hex: {buttons2:02x})")
                
                # Try to identify specific buttons
                btn_str = []
                
                # Verified Mapping
                # Byte 1
                if buttons1 & 0x01: btn_str.append("A")
                if buttons1 & 0x02: btn_str.append("B")
                if buttons1 & 0x08: btn_str.append("X")
                if buttons1 & 0x10: btn_str.append("Y")
                if buttons1 & 0x20: btn_str.append("P2 (Back)")
                if buttons1 & 0x40: btn_str.append("LB")
                if buttons1 & 0x80: btn_str.append("RB")
                
                # Byte 2
                if buttons2 & 0x01: btn_str.append("LT")
                if buttons2 & 0x02: btn_str.append("RT")
                if buttons2 & 0x04: btn_str.append("Select")
                if buttons2 & 0x08: btn_str.append("Start")
                if buttons2 & 0x10: btn_str.append("Home")
                if buttons2 & 0x20: btn_str.append("L3")
                if buttons2 & 0x40: btn_str.append("R3")
                
                print(f"Detected Inputs: {', '.join(btn_str)}")
                
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        try:
            h.close()
        except:
            pass

if __name__ == "__main__":
    visualize_controller()
