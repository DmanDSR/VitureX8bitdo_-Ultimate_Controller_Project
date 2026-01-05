import hid

TARGET_VID = 0x2DC8
TARGET_PID = 0x3208

print(f"Looking for device 0x{TARGET_VID:04x}:0x{TARGET_PID:04x}...")

devices = hid.enumerate()
found = False

for device in devices:
    if device['vendor_id'] == TARGET_VID and device['product_id'] == TARGET_PID:
        found = True
        print("\nFOUND DEVICE!")
        print(f"Manufacturer: {device.get('manufacturer_string')}")
        print(f"Product: {device.get('product_string')}")
        print(f"Usage Page: {device.get('usage_page')} (0x{device.get('usage_page'):04x})")
        print(f"Usage: {device.get('usage')} (0x{device.get('usage'):04x})")
        print(f"Path: {device.get('path')}")
        
        try:
            h = hid.device()
            h.open_path(device['path'])
            print("Opened successfully.")
            
            try:
                desc = h.get_report_descriptor()
                print(f"Report Descriptor ({len(desc)} bytes):")
                print(bytes(desc).hex())
            except Exception as e:
                print(f"Failed to get descriptor: {e}")
                
            h.close()
        except Exception as e:
            print(f"Failed to open: {e}")

if not found:
    print("Device not found in HID enumeration.")
