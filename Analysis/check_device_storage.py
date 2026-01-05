#!/usr/bin/env python3
"""
Check if the controller device has accessible storage/filesystem
"""

import os
import platform
import subprocess
from pathlib import Path

def check_windows_drives():
    """Check all Windows drives for potential controller storage"""
    print("Checking Windows drives for controller storage...")
    print("=" * 60)
    
    drives = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive_path = f"{letter}:\\"
        if os.path.exists(drive_path):
            try:
                # Try to list contents
                contents = os.listdir(drive_path)
                size = sum(
                    os.path.getsize(os.path.join(drive_path, f))
                    for f in contents
                    if os.path.isfile(os.path.join(drive_path, f))
                )
                drives.append({
                    'path': drive_path,
                    'contents': contents,
                    'size': size
                })
                print(f"\n{drive_path}")
                print(f"  Files/Folders: {len(contents)}")
                print(f"  Total size: {size} bytes")
                if contents:
                    print(f"  Contents: {', '.join(contents[:10])}")
                    if len(contents) > 10:
                        print(f"  ... and {len(contents) - 10} more")
            except PermissionError:
                print(f"{drive_path} - Access denied")
            except Exception as e:
                print(f"{drive_path} - Error: {e}")
    
    return drives

def check_linux_mounts():
    """Check Linux mount points"""
    print("Checking Linux mount points...")
    print("=" * 60)
    
    try:
        result = subprocess.run(["mount"], capture_output=True, text=True)
        print(result.stdout)
        
        # Check /media and /mnt
        for mount_dir in ["/media", "/mnt"]:
            if os.path.exists(mount_dir):
                print(f"\nChecking {mount_dir}:")
                try:
                    for item in os.listdir(mount_dir):
                        item_path = os.path.join(mount_dir, item)
                        if os.path.isdir(item_path):
                            print(f"  {item_path}/")
                            try:
                                contents = os.listdir(item_path)
                                print(f"    Contents: {', '.join(contents[:10])}")
                            except:
                                pass
                except PermissionError:
                    print(f"  Permission denied")
    except Exception as e:
        print(f"Error: {e}")

def search_for_firmware_files(root_path):
    """Search for common firmware file patterns"""
    firmware_patterns = [
        "*.bin", "*.hex", "*.fw", "*.firmware",
        "*.dfu", "*.uf2", "*.img", "*.rom",
        "config*", "firmware*", "*.cfg", "*.ini"
    ]
    
    found_files = []
    
    for pattern in firmware_patterns:
        for path in Path(root_path).rglob(pattern):
            try:
                size = path.stat().st_size
                found_files.append({
                    'path': str(path),
                    'size': size
                })
                print(f"  Found: {path} ({size} bytes)")
            except:
                pass
    
    return found_files

def main():
    system = platform.system()
    
    print("Controller Storage Detection Tool")
    print("=" * 60)
    print("\nMake sure your controller is connected via USB-C")
    print("Scanning for storage devices...\n")
    
    if system == "Windows":
        drives = check_windows_drives()
        
        print("\n" + "=" * 60)
        print("Searching for firmware files...")
        print("=" * 60)
        
        for drive in drives:
            print(f"\nSearching {drive['path']}...")
            firmware_files = search_for_firmware_files(drive['path'])
            if firmware_files:
                print(f"\nFound {len(firmware_files)} potential firmware files!")
    
    elif system == "Linux":
        check_linux_mounts()
        
        print("\n" + "=" * 60)
        print("Searching common mount points for firmware files...")
        print("=" * 60)
        
        for mount_dir in ["/media", "/mnt"]:
            if os.path.exists(mount_dir):
                firmware_files = search_for_firmware_files(mount_dir)
                if firmware_files:
                    print(f"\nFound {len(firmware_files)} potential firmware files!")
    
    else:
        print(f"Unsupported OS: {system}")
        return
    
    print("\n" + "=" * 60)
    print("If no storage device was found:")
    print("1. The firmware may be stored in non-volatile memory (not accessible as files)")
    print("2. You may need to use specialized tools to access the device's memory")
    print("3. Check the device manufacturer's documentation for firmware update tools")

if __name__ == "__main__":
    main()


