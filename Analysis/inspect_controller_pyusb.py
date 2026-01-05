#!/usr/bin/env python3
"""
Direct USB device inspection using pyusb
This bypasses the HID library issues on Windows
"""

import usb.core
import usb.util

# VITURE x 8BitDo controller identifiers
TARGET_VID = 0x2DC8
TARGET_PID = 0x301F

def inspect_device():
    """Inspect the controller using pyusb"""
    print("VITURE x 8BitDo Controller Inspector")
    print("=" * 60)
    
    # Find the device
    device = usb.core.find(idVendor=TARGET_VID, idProduct=TARGET_PID)
    
    if device is None:
        print(f"Controller not found!")
        print(f"Looking for VID: 0x{TARGET_VID:04X}, PID: 0x{TARGET_PID:04X}")
        print("\nMake sure the controller is connected via USB-C")
        return
    
    print(f"\n>>> Controller Found! <<<")
    print("=" * 60)
    
    try:
        # Get device information
        print(f"\nDevice Information:")
        print(f"  Vendor ID: 0x{device.idVendor:04X}")
        print(f"  Product ID: 0x{device.idProduct:04X}")
        print(f"  Bus: {device.bus}")
        print(f"  Address: {device.address}")
        
        # Get device descriptor
        print(f"\nDevice Descriptor:")
        print(f"  USB Version: {device.bcdUSB >> 8}.{(device.bcdUSB >> 4) & 0x0F}.{device.bcdUSB & 0x0F}")
        print(f"  Device Class: {device.bDeviceClass}")
        print(f"  Device Subclass: {device.bDeviceSubClass}")
        print(f"  Device Protocol: {device.bDeviceProtocol}")
        print(f"  Max Packet Size: {device.bMaxPacketSize0}")
        print(f"  Number of Configurations: {device.bNumConfigurations}")
        
        # Get string descriptors
        try:
            print(f"\nString Descriptors:")
            print(f"  Manufacturer: {usb.util.get_string(device, device.iManufacturer)}")
            print(f"  Product: {usb.util.get_string(device, device.iProduct)}")
            if device.iSerialNumber:
                print(f"  Serial: {usb.util.get_string(device, device.iSerialNumber)}")
        except Exception as e:
            print(f"  Could not read strings: {e}")
        
        # Get configuration descriptors
        print(f"\nConfiguration Information:")
        for cfg in device:
            print(f"\n  Configuration {cfg.bConfigurationValue}:")
            print(f"    Interfaces: {cfg.bNumInterfaces}")
            print(f"    Max Power: {cfg.bMaxPower * 2}mA")
            if cfg.iConfiguration:
                try:
                    print(f"    Description: {usb.util.get_string(device, cfg.iConfiguration)}")
                except:
                    pass
            
            # Get interface descriptors
            for intf in cfg:
                print(f"\n    Interface {intf.bInterfaceNumber}:")
                print(f"      Class: {intf.bInterfaceClass} (0x{intf.bInterfaceClass:02X})")
                print(f"      Subclass: {intf.bInterfaceSubClass}")
                print(f"      Protocol: {intf.bInterfaceProtocol}")
                print(f"      Endpoints: {intf.bNumEndpoints}")
                
                # Check if it's a HID interface
                if intf.bInterfaceClass == 3:  # HID class
                    print(f"      >>> This is a HID interface! <<<")
                
                # Get endpoint descriptors
                for ep in intf:
                    direction = "IN" if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN else "OUT"
                    transfer_type = ["Control", "Isochronous", "Bulk", "Interrupt"][ep.bmAttributes & 0x03]
                    print(f"        Endpoint 0x{ep.bEndpointAddress:02X} ({direction}, {transfer_type})")
                    print(f"          Max Packet Size: {ep.wMaxPacketSize}")
                    if transfer_type == "Interrupt":
                        print(f"          Polling Interval: {ep.bInterval}ms")
        
        # Try to read HID report descriptor if available
        print(f"\n" + "=" * 60)
        print("Attempting to read HID report descriptor...")
        print("=" * 60)
        
        try:
            # Set configuration
            device.set_configuration()
            
            # Find HID interface
            for cfg in device:
                for intf in cfg:
                    if intf.bInterfaceClass == 3:  # HID class
                        print(f"\nFound HID interface {intf.bInterfaceNumber}")
                        
                        # Try to get report descriptor
                        try:
                            # HID report descriptor request
                            # bmRequestType: 0x81 (Device to host, standard, device)
                            # bRequest: 0x06 (GET_DESCRIPTOR)
                            # wValue: 0x2200 (Report descriptor, index 0)
                            # wIndex: interface number
                            report_desc = device.ctrl_transfer(
                                0x81,  # bmRequestType
                                0x06,  # bRequest (GET_DESCRIPTOR)
                                0x2200,  # wValue (Report descriptor)
                                intf.bInterfaceNumber,  # wIndex
                                256  # wLength
                            )
                            
                            print(f"Report Descriptor Length: {len(report_desc)} bytes")
                            print(f"Report Descriptor (hex): {report_desc.hex()}")
                            print(f"Report Descriptor (first 64 bytes):")
                            for i in range(0, min(64, len(report_desc)), 16):
                                hex_str = ' '.join(f'{b:02X}' for b in report_desc[i:i+16])
                                ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in report_desc[i:i+16])
                                print(f"  {i:04X}: {hex_str:<48} {ascii_str}")
                            
                        except Exception as e:
                            print(f"Could not read report descriptor: {e}")
        
        except Exception as e:
            print(f"Error setting configuration: {e}")
        
    except Exception as e:
        print(f"Error inspecting device: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Release the device
        try:
            usb.util.dispose_resources(device)
        except:
            pass

if __name__ == "__main__":
    try:
        inspect_device()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Inspection complete!")

