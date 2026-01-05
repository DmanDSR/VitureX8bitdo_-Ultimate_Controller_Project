import vgamepad as vg
import hid
import time
import sys

# Constants for controller mapping - CORRECTED based on User Diagnostics
# Byte 1 (b1)
HID_BTN_A       = 0x01  # Assumed
HID_BTN_B       = 0x02  # Assumed
HID_BTN_X       = 0x08  # Confirmed
HID_BTN_Y       = 0x10  # Confirmed
HID_BTN_LB      = 0x40  # Swapped per User Report
HID_BTN_RB      = 0x80  # Confirmed

# Byte 2 (b2)
HID_BTN_LT      = 0x01  # Swapped per User Report
HID_BTN_RT      = 0x02  # Confirmed (Digital flag)
HID_BTN_SELECT  = 0x04  # Confirmed (In standard Xbox map, this is "Back")
HID_BTN_START   = 0x08  # Confirmed
HID_BTN_HOME    = 0x10  # Confirmed
HID_BTN_L3      = 0x20  # Confirmed
HID_BTN_R3      = 0x40  # Confirmed

HID_VID = 0x2DC8
HID_PID = 0x301F

DEADZONE_THRESHOLD = 0.08  # 8% deadzone (Standard for controllers)

def scale_axis(val):
    """Scale 0-255 (unsigned) to -32768 to 32767 (signed 16-bit) with Deadzone"""
    # 1. Center the value (0-255 -> -1.0 to 1.0)
    # Center is technically 127.5, but 128 is common midpoint
    normalized = (val - 128) / 127.5
    
    # 2. Apply Deadzone
    if abs(normalized) < DEADZONE_THRESHOLD:
        return 0
        
    # 3. Rescale remaining range to 0.0 to 1.0 so we don't jump
    # (optional, but feels smoother)
    if normalized > 0:
        normalized = (normalized - DEADZONE_THRESHOLD) / (1 - DEADZONE_THRESHOLD)
    else:
        normalized = (normalized + DEADZONE_THRESHOLD) / (1 - DEADZONE_THRESHOLD)
        
    # 4. Convert to 16-bit integer
    return int(normalized * 32767)

def scale_inv_axis(val):
    """Invert axis with deadzone support"""
    return -scale_axis(val)

def parse_hat_switch(hat_value):
    """Parse HID hat switch value to D-pad directions"""
    # 0x0F is center, 0x1F seems to be special (Turbo?), 0-7 are directions
    if hat_value >= 8:
        return (False, False, False, False)
    
    directions = [
        (True, False, False, False),   # 0: Up
        (True, False, False, True),    # 1: Up-Right
        (False, False, False, True),   # 2: Right
        (False, True, False, True),    # 3: Down-Right
        (False, True, False, False),   # 4: Down
        (False, True, True, False),    # 5: Down-Left
        (False, False, True, False),   # 6: Left
        (True, False, True, False),    # 7: Up-Left
    ]
    
    return directions[hat_value] if hat_value < 8 else (False, False, False, False)

def find_device():
    """Find the VITURE controller path"""
    # Try finding exact usage mode first
    for device in hid.enumerate():
        if device['vendor_id'] == HID_VID and device['product_id'] == HID_PID:
                if device['usage_page'] == 1 and device['usage'] == 5:
                    return device['path']
    
    # Fallback to any interface
    for device in hid.enumerate():
        if device['vendor_id'] == HID_VID and device['product_id'] == HID_PID:
            return device['path']
    return None

def main():
    print("VITURE x 8BitDo -> Virtual Xbox 360 Bridge")
    print("Version: User-Mapped Fix + Auto-Reconnect")
    print(f"Deadzone: {int(DEADZONE_THRESHOLD*100)}% active")
    print("------------------------------------------")

    # 1. Initialize Virtual Controller
    try:
        gamepad = vg.VX360Gamepad()
        print("Virtual Xbox 360 Controller created successfully.")
    except Exception as e:
        print(f"Failed to create virtual gamepad: {e}")
        print("Make sure ViGEmBus drivers are installed!")
        sys.exit(1)

    print("\nBRIDGE ACTIVE! Press Ctrl+C to stop.")
    print("Your PC should now see an Xbox 360 Controller.")

    while True:
        try:
            # 2. Connect to Physical Controller
            print("\nSearching for controller...")
            target_path = None
            while target_path is None:
                target_path = find_device()
                if target_path is None:
                    time.sleep(1) # Wait before retry
            
            print(f"Found controller! Connecting...")
            h = hid.device()
            h.open_path(target_path)
            h.set_nonblocking(1)
            print(f"Connected to physical controller at {HID_VID:04x}:{HID_PID:04x}")

            # 3. Main Input Loop
            while True:
                # Read 64 bytes
                try:
                    report = h.read(64)
                except OSError:
                    print("Device disconnected (read error).")
                    break
                
                if not report:
                    # No data, just sleep and check again (non-blocking)
                    time.sleep(0.005)
                    continue

                if len(report) >= 8:
                    b1 = report[1]
                    b2 = report[2]
                    hat = report[3]
                    
                    gamepad.reset()
                    
                    # --- Button Mappings (Based on User Diagnostics) ---
                    
                    # Face Buttons
                    if b1 & HID_BTN_A: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                    if b1 & HID_BTN_B: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
                    if b1 & HID_BTN_X: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
                    if b1 & HID_BTN_Y: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
                    
                    # Bumpers (Shoulders)
                    if b1 & HID_BTN_LB: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
                    if b1 & HID_BTN_RB: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
                    
                    # Triggers (Digital input converted to full Analog press)
                    if b2 & HID_BTN_LT: gamepad.left_trigger(255)
                    if b2 & HID_BTN_RT: gamepad.right_trigger(255)
                    
                    # System Buttons
                    if b2 & HID_BTN_SELECT: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
                    if b2 & HID_BTN_START:  gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
                    if b2 & HID_BTN_HOME:   gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
                    
                    # Thumbstick Clicks
                    if b2 & HID_BTN_L3:     gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
                    if b2 & HID_BTN_R3:     gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
                    
                    # D-Pad
                    d_up, d_down, d_left, d_right = parse_hat_switch(hat)
                    if d_up:    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
                    if d_down:  gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
                    if d_left:  gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
                    if d_right: gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
                    
                    # Analog Sticks (Standard HID locations)
                    lx = scale_axis(report[4])
                    ly = scale_inv_axis(report[5])
                    rx = scale_axis(report[6])
                    ry = scale_inv_axis(report[7])
                    
                    gamepad.left_joystick(x_value=lx, y_value=ly)
                    gamepad.right_joystick(x_value=rx, y_value=ry)
                    
                    gamepad.update()
                
                # Polling rate ~200Hz
                time.sleep(0.005)
                
            # Loop broke (disconnected), close device and go back to searching
            h.close()
            time.sleep(1)

        except KeyboardInterrupt:
            print("\nStopping bridge based on user input...")
            break
        except Exception as e:
            print(f"\nUnexpected Error: {e}")
            time.sleep(2) # Wait a bit before retrying main loop
            
    try:
        h.close()
    except:
        pass

if __name__ == "__main__":
    main()
