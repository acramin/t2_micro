# t2_micro

D&D Dice Roller Application for Raspberry Pi with Touchscreen

## Features
- Character profile management with ability scores, skills, and weapons
- Multiple dice rolling options (d4, d6, d8, d10, d12, d20, d100)
- Attack rolls, saving throws, and ability checks
- Motion sensor integration for hands-free rolling
- Touchscreen-friendly interface

## Touchscreen Keyboard Configuration

The app is configured to display an on-screen virtual keyboard when you tap on text input fields. The keyboard is set to `systemanddock` mode, which shows Kivy's virtual keyboard docked at the bottom of the screen.

### Troubleshooting Keyboard Issues

If the keyboard doesn't appear when you tap on a text field:

1. **Clear Kivy's cached config**: Delete the file `~/.kivy/config.ini` (on Raspberry Pi, this is typically `/home/pi/.kivy/config.ini`)
   ```bash
   rm ~/.kivy/config.ini
   ```

2. **Restart the application** after deleting the config file

3. **Alternative keyboard modes** (if you want to change it):
   - Edit `app.py` and change the line:
     ```python
     Config.set('kivy', 'keyboard_mode', 'dock')
     ```
   - Options:
     - `'dock'` - Kivy keyboard docked at bottom (recommended for touchscreen)
     - `'systemanddock'` - Uses both Kivy and system keyboards (requires external desktop keyboard support)
     - `'system'` - Uses system keyboard only
     - `''` - Auto-detect based on platform

4. **For debugging**: Check if the keyboard config is being loaded by looking at the console output when the app starts

## Motion Sensor Configuration

- Default settle time: 30 seconds (configurable in `utils/motion_sensor.py`)
- GPIO pin: 17 (BCM mode)

## Running the Application

```bash
python app.py
```