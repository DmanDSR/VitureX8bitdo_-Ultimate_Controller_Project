#!/usr/bin/env python3
"""
USB Device Detection Script
Detects and lists all USB devices, specifically looking for gamepad/controller devices.
"""

import sys
import platform

def detect_usb_devices_windows():
    """Detect USB devices on Windows using PowerShell"""
    import subprocess
    
    print("Detecting USB devices on Windows...")
    print("=" * 60)
    
    # Get USB devices using PowerShell
    ps_command = """
    Get-PnpDevice -Class USB | Where-Object { $_.Status -eq 'OK' } | 
    Select-Object FriendlyName, InstanceId, Status | 
    Format-Table -AutoSize
    """
    
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_command],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running PowerShell command: {e}")

def detect_usb_devices_linux():
    """Detect USB devices on Linux using lsusb"""
    import subprocess
    
    print("Detecting USB devices on Linux...")
    print("=" * 60)
    
    try:
        result = subprocess.run(["lsusb"], capture_output=True, text=True)
        print(result.stdout)
        
        # Also check /dev/input for gamepad devices
        print("\nChecking for gamepad devices in /dev/input...")
        result = subprocess.run(["ls", "-la", "/dev/input/"], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")

def detect_hid_devices():
    """Try to detect HID devices specifically"""
    try:
        import hid
        print("\n" + "=" * 60)
        print("HID Devices (using pyhidapi):")
        print("=" * 60)
        
        # VITURE x 8BitDo controller identifiers
        TARGET_VID = 0x2DC8
        TARGET_PID = 0x301F
        
        devices = hid.enumerate()
        found_target = False
        
        for device in devices:
            vid = device.get('vendor_id', 0)
            pid = device.get('product_id', 0)
            is_target = (vid == TARGET_VID and pid == TARGET_PID)
            
            if is_target:
                found_target = True
                print(f"\n{'='*60}")
                print(">>> VITURE x 8BitDo Controller FOUND! <<<")
                print(f"{'='*60}")
            
            if is_target or 'gamepad' in str(device.get('product', '')).lower() or \
               'controller' in str(device.get('product', '')).lower() or \
               device.get('usage_page') == 1:  # Generic Desktop Controls
                print(f"\nDevice: {device.get('manufacturer_string', 'Unknown')} {device.get('product_string', 'Unknown')}")
                print(f"  Vendor ID: 0x{vid:04x}")
                print(f"  Product ID: 0x{pid:04x}")
                if is_target:
                    print(f"  >>> This is your VITURE x 8BitDo controller! <<<")
                print(f"  Path: {device.get('path', 'N/A')}")
                print(f"  Serial: {device.get('serial_number', 'N/A')}")
        
        if not found_target:
            print(f"\nNote: VITURE x 8BitDo controller (VID: 0x{TARGET_VID:04x}, PID: 0x{TARGET_PID:04x}) not detected.")
            print("Make sure the controller is connected via USB-C.")
    except ImportError:
        print("\nNote: Install 'hid' package for HID device detection:")
        print("  pip install hid")
    except Exception as e:
        print(f"Error detecting HID devices: {e}")

def check_storage_devices():
    """Check if any USB devices appear as storage devices"""
    print("\n" + "=" * 60)
    print("Checking for USB storage devices...")
    print("=" * 60)
    
    system = platform.system()
    
    if system == "Windows":
        import subprocess
        ps_command = """
        Get-PSDrive -PSProvider FileSystem | 
        Where-Object { $_.Used -gt 0 } | 
        Select-Object Name, Root, Used, Free | 
        Format-Table -AutoSize
        """
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            print(result.stdout)
        except Exception as e:
            print(f"Error: {e}")
    elif system == "Linux":
        import subprocess
        try:
            result = subprocess.run(["lsblk"], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("USB Device Detection Tool")
    print("=" * 60)
    
    system = platform.system()
    
    if system == "Windows":
        detect_usb_devices_windows()
    elif system == "Linux":
        detect_usb_devices_linux()
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)
    
    detect_hid_devices()
    check_storage_devices()
    
    print("\n" + "=" * 60)
    print("Next steps:")
    print("1. Look for your controller in the list above")
    print("2. Note the Vendor ID and Product ID")
    print("3. Check if it appears as a storage device")
    print("4. Run check_device_storage.py to try accessing files")
