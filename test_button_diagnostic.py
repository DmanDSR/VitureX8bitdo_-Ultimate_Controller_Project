#!/usr/bin/env python3
"""
Button Diagnostic Tool
Shows raw byte values to help map buttons correctly
"""

import sys
import time

def test_button_diagnostic():
    try:
        import hid
    except ImportError:
        print("Error: 'hid' package not installed")
        return

    TARGET_VID = 0x2DC8
    TARGET_PID = 0x301F

    print("=" * 70)
    print("BUTTON DIAGNOSTIC - Press ONE button at a time")
    print("=" * 70)
    print("This will show the raw byte values for each button press")
    print("Press Ctrl+C to stop\n")
    
    # Find the device
    target_device = None
    for device in hid.enumerate():
        if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
            if device['usage_page'] == 1 and device['usage'] == 5:
                target_device = device
                break
    
    if not target_device:
        for device in hid.enumerate():
            if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
                target_device = device
                break
    
    if not target_device:
        print("[X] Controller not found!")
        return

    print("[OK] Controller found!\n")
    print("Press ONE button and HOLD it, then note the values below")
    print("Release and press the next button\n")
    print("-" * 70)

    try:
        h = hid.device()
        h.open_path(target_device['path'])
        h.set_nonblocking(1)
        
        last_data = None
        
        while True:
            data = h.read(64)
            if data and len(data) >= 8:
                # Only show when data changes
                if data != last_data:
                    last_data = data
                    
                    b1 = data[1]
                    b2 = data[2]
                    hat = data[3]
                    
                    # Clear and show
                    sys.stdout.write("\033[H\033[J")
                    print("=" * 70)
                    print("BUTTON DIAGNOSTIC")
                    print("=" * 70)
                    print()
                    print(f"Byte 1: {b1:02x} ({b1:08b})")
                    print(f"Byte 2: {b2:02x} ({b2:08b})")
                    print(f"Byte 3 (Hat): {hat:02x} ({hat:08b})")
                    print()
                    print("Full first 10 bytes:")
                    hex_str = " ".join([f"{b:02x}" for b in data[:10]])
                    print(f"  {hex_str}")
                    print()
                    print("=" * 70)
                    print("Press ONE button and HOLD it to see its values")
                    print("=" * 70)
            
            time.sleep(0.001)  # Very small delay to prevent excessive CPU

    except KeyboardInterrupt:
        print("\n\nStopped.")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        try:
            h.close()
        except:
            pass

if __name__ == "__main__":
    test_button_diagnostic()

