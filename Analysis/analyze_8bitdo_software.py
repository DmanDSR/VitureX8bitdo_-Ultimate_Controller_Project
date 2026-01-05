#!/usr/bin/env python3
"""
Analyze 8BitDo Ultimate Software V2 for firmware update capabilities
"""

import os
import json
import subprocess
from pathlib import Path

SOFTWARE_DIR = Path("8BitDo_Ultimate_Software_V2_Windows_V1.29/8BitDo_Ultimate_Software_V2_Windows_V1.29")

def analyze_software():
    """Analyze the 8BitDo software installation"""
    print("8BitDo Ultimate Software V2 Analysis")
    print("=" * 60)
    
    if not SOFTWARE_DIR.exists():
        print(f"Software directory not found: {SOFTWARE_DIR}")
        return
    
    print(f"\nSoftware Location: {SOFTWARE_DIR.absolute()}")
    
    # Check for key files
    print("\n" + "=" * 60)
    print("Key Files Found:")
    print("=" * 60)
    
    key_files = {
        "Main Executable": "8BitDo Ultimate Software V2.exe",
        "DFU Tool": "dfu4.exe",
        "HID Library": "RTKHIDKit.dll",
        "Advance DLL": "8BitDoAdvance.dll",
        "Config": "8BitDo Ultimate Software V2.dll.config"
    }
    
    for desc, filename in key_files.items():
        filepath = SOFTWARE_DIR / filename
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  [OK] {desc}: {filename} ({size:,} bytes)")
        else:
            print(f"  [MISSING] {desc}: {filename} (NOT FOUND)")
    
    # Check log files
    print("\n" + "=" * 60)
    print("Log Files Analysis:")
    print("=" * 60)
    
    log_dir = SOFTWARE_DIR / "Log"
    if log_dir.exists():
        log_files = list(log_dir.glob("*.txt"))
        print(f"  Found {len(log_files)} log files:")
        for log_file in sorted(log_files)[-3:]:  # Show last 3
            print(f"    - {log_file.name}")
            try:
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if "PID" in content or "VID" in content:
                        lines = [l for l in content.split('\n') if 'PID' in l or 'VID' in l]
                        if lines:
                            print(f"      Sample: {lines[0][:80]}")
            except:
                pass
    
    # Check error log
    print("\n" + "=" * 60)
    print("Error Log Analysis:")
    print("=" * 60)
    
    err_log = SOFTWARE_DIR / "ErrLog" / "ErrLog.txt"
    if err_log.exists():
        try:
            with open(err_log, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                print(f"  Error log size: {len(content)} bytes")
                
                # Look for firmware update information
                if "firmware" in content.lower() or "version" in content.lower():
                    print("  >>> Contains firmware/version information! <<<")
                    
                    # Try to extract JSON
                    lines = content.split('\n')
                    for line in lines:
                        if line.strip().startswith('{'):
                            try:
                                data = json.loads(line)
                                if 'list' in data and data['list']:
                                    print(f"\n  Firmware Update Information:")
                                    for item in data['list']:
                                        print(f"    Version: {item.get('version', 'N/A')}")
                                        print(f"    Date: {item.get('date', 'N/A')}")
                                        print(f"    File: {item.get('fileName', 'N/A')}")
                                        print(f"    Size: {item.get('fileSize', 0):,} bytes")
                                        print(f"    MD5: {item.get('md5', 'N/A')}")
                                        print(f"    Type: {item.get('type', 'N/A')}")
                                        if 'readme' in item:
                                            print(f"    Readme: {item['readme']}")
                                        print()
                            except:
                                pass
        except Exception as e:
            print(f"  Error reading log: {e}")
    
    # Check for DFU tool
    print("\n" + "=" * 60)
    print("DFU Tool Analysis:")
    print("=" * 60)
    
    dfu_tool = SOFTWARE_DIR / "dfu4.exe"
    if dfu_tool.exists():
        print(f"  [OK] DFU tool found: dfu4.exe")
        print(f"    This is a Device Firmware Update tool!")
        print(f"    Size: {dfu_tool.stat().st_size:,} bytes")
        print(f"\n    DFU tools can:")
        print(f"      - Read firmware from device")
        print(f"      - Write firmware to device")
        print(f"      - Potentially extract firmware for analysis")
    
    # Check for data directory
    print("\n" + "=" * 60)
    print("Data Directory Analysis:")
    print("=" * 60)
    
    data_dir = SOFTWARE_DIR / "data"
    if data_dir.exists():
        print(f"  Data directory contents:")
        for item in data_dir.iterdir():
            if item.is_file():
                print(f"    - {item.name} ({item.stat().st_size:,} bytes)")
    
    # Check versions.txt (might be binary)
    versions_file = data_dir / "versions.txt" if data_dir.exists() else None
    if versions_file and versions_file.exists():
        print(f"\n  versions.txt found (may be binary)")
        size = versions_file.stat().st_size
        print(f"    Size: {size:,} bytes")
        if size < 10000:  # Try to read if small
            try:
                with open(versions_file, 'rb') as f:
                    data = f.read()
                    # Try to find readable strings
                    strings = [s.decode('utf-8', errors='ignore') for s in data.split(b'\x00') if len(s) > 3]
                    if strings:
                        print(f"    Contains strings:")
                        for s in strings[:10]:
                            print(f"      - {s}")
            except:
                pass
    
    print("\n" + "=" * 60)
    print("Recommendations:")
    print("=" * 60)
    print("1. The dfu4.exe tool may be able to read/write firmware")
    print("2. Check if the software detects your controller when running")
    print("3. Look for firmware update options in the GUI")
    print("4. The RTKHIDKit.dll suggests Realtek HID support")
    print("5. Firmware files may be downloaded from 8BitDo servers")

if __name__ == "__main__":
    analyze_software()

