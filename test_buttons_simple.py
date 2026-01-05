#!/usr/bin/env python3
"""
Simple Button Tester
Shows which buttons are pressed in a clean, simple format
"""

import hid
import time
import sys
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("VITURE x 8BitDo - Simple Button Tester")
    print("--------------------------------------")
    
    # Define the CORRECTED mapping found via diagnostics
    # Format: (Bitmask, ByteIndex, Name)
    # ByteIndex 0 = Report ID (ignore), Byte 1 = Buttons A, Byte 2 = Buttons B
    
    BUTTON_MAP = [
        # Byte 1 Buttons
        (0x01, 1, "A"),             # Assumed based on standard patterns
        (0x02, 1, "B"),             # Assumed based on standard patterns
        (0x08, 1, "X"),             # Confirmed
        (0x10, 1, "Y"),             # Confirmed
        (0x20, 1, "P2 (Back Btn)"), # Confirmed
        (0x40, 1, "LB"),            # Swapped per User Report
        (0x80, 1, "RB"),            # Confirmed
        
        # Byte 2 Buttons
        (0x01, 2, "LT"),            # Swapped per User Report
        (0x02, 2, "RT"),            # Confirmed(!!)
        (0x04, 2, "Select/Minus"),  # Confirmed
        (0x08, 2, "Start/Plus"),    # Confirmed
        (0x10, 2, "Home/V"),        # Confirmed
        (0x20, 2, "L3 (Stick)"),    # Confirmed
        (0x40, 2, "R3 (Stick)"),    # Confirmed
    ]

    HID_VID = 0x2DC8
    HID_PID = 0x301F

    try:
        h = hid.device()
        
        # Connect
        target_path = None
        for device in hid.enumerate():
            if device['vendor_id'] == HID_VID and device['product_id'] == HID_PID:
                 if device['usage_page'] == 1 and device['usage'] == 5:
                     target_path = device['path']
                     break
        
        if not target_path:
            # Fallback
            for device in hid.enumerate():
                if device['vendor_id'] == HID_VID and device['product_id'] == HID_PID:
                    target_path = device['path']
                    break
                    
        if not target_path:
            print("Controller not found.")
            sys.exit(1)
            
        h.open_path(target_path)
        h.set_nonblocking(1)
        print("Connected! Press buttons to test (Ctrl+C to stop)")
        time.sleep(1)

        while True:
            report = h.read(64)
            if report and len(report) >= 8:
                # Clear screen to minimize stutter
                sys.stdout.write("\033[H\033[J")
                
                print("VITURE Controller Input Monitor")
                print("===============================")
                print(f"Raw: {report[1]:02x} {report[2]:02x} {report[3]:02x}")
                print("-------------------------------")
                
                # Check Buttons
                active_buttons = []
                for mask, byte_idx, name in BUTTON_MAP:
                    if report[byte_idx] & mask:
                        active_buttons.append(f"[ {name} ]")
                
                if active_buttons:
                    print("PRESSED: " + " ".join(active_buttons))
                else:
                    print("PRESSED: (None)")
                
                # Check D-Pad
                hat = report[3]
                directions = ["Up", "Up-Right", "Right", "Down-Right", "Down", "Down-Left", "Left", "Up-Left"]
                if hat < 8:
                    print(f"D-PAD:   {directions[hat]}")
                elif hat == 0x0F:
                    print(f"D-PAD:   Centered")
                else:
                    print(f"D-PAD:   Value {hat:02x}")
                
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nStopping...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        try:
            h.close()
        except:
            pass

if __name__ == "__main__":
    main()
