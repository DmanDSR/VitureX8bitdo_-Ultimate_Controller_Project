#!/usr/bin/env python3
"""
Controller Input Tester
Reads raw HID reports from the VITURE x 8BitDo controller and prints them.
"""

import sys
import time

def test_input():
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
            # We want the interface with Usage Page 1, Usage 5 (Game Pad)
            if device['usage_page'] == 1 and device['usage'] == 5:
                target_device = device
                break
            # Fallback: just take the first one if we can't distinguish
            if target_device is None:
                target_device = device
    
    if not target_device:
        print("Controller not found.")
        return

    print(f"Found device: {target_device['product_string']}")
    print(f"Path: {target_device['path']}")
    print("\nListening for inputs... (Press Ctrl+C to stop)")
    print("Each line represents a data packet from the controller.")
    print("-" * 60)

    try:
        h = hid.device()
        h.open_path(target_device['path'])
        
        # Set non-blocking
        h.set_nonblocking(1)

        last_print = 0
        
        while True:
            # Read up to 64 bytes
            data = h.read(64)
            if data:
                # Convert to hex string
                hex_data = " ".join([f"{b:02x}" for b in data])
                print(f"Data: {hex_data}")
            
            time.sleep(0.01)

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
    test_input()
