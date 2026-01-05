# Bridge Scripts

Main controller bridge/driver scripts that convert VITURE controller input to Xbox 360 controller format.

## Files

- **controller_bridge.py** - Main bridge script (currently same as fixed version, button mappings need correction)
- **controller_bridge_fixed.py** - Work in progress version (button mappings need correction)

**Note:** Both files currently have the same content. The button mappings need to be corrected based on diagnostic testing.

## Usage

```bash
python controller_bridge.py
```

Requires:
- ViGEmBus driver installed
- Python packages: `vgamepad`, `hid` (or `hidapi`)

