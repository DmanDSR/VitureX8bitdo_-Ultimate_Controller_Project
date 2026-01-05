#!/usr/bin/env python3
"""
HID Device Inspector
Examines HID device capabilities and reports to help understand controller functionality
"""

import sys

def inspect_hid_device():
    """Inspect HID device capabilities"""
    try:
        import hid
    except ImportError:
        print("Error: 'hid' package not installed")
        print("Install it with: pip install hid")
        return
    
    print("HID Device Inspector")
    print("=" * 60)
    print("\nScanning for HID devices...\n")
    
    devices = hid.enumerate()
    
    if not devices:
        print("No HID devices found")
        return
    
    # VITURE x 8BitDo controller identifiers
    TARGET_VID = 0x2DC8
    TARGET_PID = 0x301F
    
    # Filter for gamepad/controller devices
    controller_devices = []
    for device in devices:
        vid = device.get('vendor_id', 0)
        pid = device.get('product_id', 0)
        product = str(device.get('product_string', '')).lower()
        manufacturer = str(device.get('manufacturer_string', '')).lower()
        usage_page = device.get('usage_page', 0)
        
        # Always include the target controller if found
        is_target = (vid == TARGET_VID and pid == TARGET_PID)
        
        if is_target or 'gamepad' in product or 'controller' in product or \
           'gamepad' in manufacturer or 'controller' in manufacturer or \
           usage_page == 1:  # Generic Desktop Controls
            controller_devices.append(device)
    
    if not controller_devices:
        print("No controller/gamepad devices found")
        print("\nAll HID devices:")
        for device in devices[:5]:  # Show first 5
            print(f"  - {device.get('manufacturer_string', 'Unknown')} {device.get('product_string', 'Unknown')}")
        return
    
    print(f"Found {len(controller_devices)} controller/gamepad device(s):\n")
    
    for i, device in enumerate(controller_devices, 1):
        vid = device.get('vendor_id', 0)
        pid = device.get('product_id', 0)
        is_target = (vid == TARGET_VID and pid == TARGET_PID)
        
        print(f"Device {i}:")
        print("=" * 60)
        if is_target:
            print(">>> VITURE x 8BitDo Ultimate Mobile Gaming Controller <<<")
            print("=" * 60)
        print(f"Manufacturer: {device.get('manufacturer_string', 'Unknown')}")
        print(f"Product: {device.get('product_string', 'Unknown')}")
        print(f"Vendor ID: 0x{vid:04x}")
        print(f"Product ID: 0x{pid:04x}")
        if is_target:
            print("  >>> This is your target controller! <<<")
        print(f"Serial Number: {device.get('serial_number', 'N/A')}")
        print(f"Usage Page: {device.get('usage_page', 'N/A')}")
        print(f"Usage: {device.get('usage', 'N/A')}")
        print(f"Interface Number: {device.get('interface_number', 'N/A')}")
        print(f"Path: {device.get('path', 'N/A')}")
        
        # Try to open the device and get report descriptor
        try:
            h = hid.device()
            h.open_path(device['path'])
            
            print(f"\nDevice opened successfully!")
            print(f"Manufacturer String: {h.get_manufacturer_string()}")
            print(f"Product String: {h.get_product_string()}")
            print(f"Serial Number: {h.get_serial_number_string()}")
            
            # Get report descriptor
            try:
                report_desc = h.get_report_descriptor()
                print(f"\nReport Descriptor Length: {len(report_desc)} bytes")
                print(f"Report Descriptor (hex): {bytes(report_desc).hex()}")
                
                # Try to parse basic info
                if len(report_desc) > 0:
                    print("\nRaw descriptor analysis:")
                    print(f"  First bytes: {bytes(report_desc)[:20].hex()}")
            except Exception as e:
                print(f"\nCould not read report descriptor: {e}")
            
            h.close()
        except Exception as e:
            print(f"\nCould not open device: {e}")
        
        print()

def save_device_info():
    """Save device information to a file for analysis"""
    try:
        import hid
        import json
        
        devices = hid.enumerate()
        device_info = []
        
        for device in devices:
            info = {
                'vendor_id': device.get('vendor_id'),
                'product_id': device.get('product_id'),
                'manufacturer': device.get('manufacturer_string'),
                'product': device.get('product_string'),
                'serial': device.get('serial_number'),
                'usage_page': device.get('usage_page'),
                'usage': device.get('usage'),
                'path': str(device.get('path', ''))
            }
            device_info.append(info)
        
        with open('device_info.json', 'w') as f:
            json.dump(device_info, f, indent=2)
        
        print("\nDevice information saved to device_info.json")
    except Exception as e:
        print(f"Error saving device info: {e}")

if __name__ == "__main__":
    inspect_hid_device()
    save_device_info()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Note the Vendor ID and Product ID of your controller")
    print("2. The report descriptor contains information about device capabilities")
    print("3. Use this information to understand what the device can do")
    print("4. Check if there are firmware update tools available for this device")


