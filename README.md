# t2_micro

D&D Dice Roller Application for Raspberry Pi with Touchscreen

## Features
- Character profile management with ability scores, skills, and weapons
- Multiple dice rolling options (d4, d6, d8, d10, d12, d20, d100)
- Attack rolls, saving throws, and ability checks
- Motion sensor integration for hands-free rolling
- Touchscreen-friendly interface

## Touchscreen Keyboard Configuration

The app ships with a **custom on-screen keyboard** that appears the moment a text field gains focus. It occupies the lower half of the display, supports letters, numbers, space, backspace, shift (case toggle), and quick hide/enter actions. Because this keyboard is implemented entirely in-app, it works consistently on Raspberry Pi touchscreens regardless of the underlying window manager.

### Keyboard Behavior

- **Half-screen layout**: anchored to the bottom, leaving the upper half visible for the form
- **Single-tap activation**: tapping any white text field focuses it and slides the keyboard in
- **Shared keyboard**: stays visible as you hop between fields; tap above the keyboard to dismiss
- **Shift toggle**: tap **SHIFT** to switch between lower- and upper-case characters

### Custom TextInput Implementation

Every text field uses `PersistentKeyboardTextInput`, which coordinates with the shared keyboard controller to:
1. Trigger the keyboard on first tap
2. Keep focus locked on the active field while pressing keys
3. Close the keyboard only when you tap the **Hide** button or outside the keyboard area

### Troubleshooting Keyboard Issues

If the keyboard ever fails to appear:

1. **Clear Kivy's cached config**: delete `~/.kivy/config.ini` (typically `/home/pi/.kivy/config.ini`)
  ```bash
  rm ~/.kivy/config.ini
  ```

2. **Restart the application** after deleting the config file

3. **Confirm build includes new modules**: ensure `components/virtual_keyboard.py` and `components/text_inputs.py` are present on the device and imported in `app.py`

4. **Check console logs**: any exceptions logged during keyboard creation will be printed to stdout/stderr

## Motion Sensor Configuration

- Default settle time: 30 seconds (configurable in `utils/motion_sensor.py`)
- GPIO pin: 17 (BCM mode)

## Running the Application

```bash
python app.py
```