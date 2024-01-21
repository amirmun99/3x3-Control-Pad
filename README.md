# 3x3-Control-Pad
A 9 Keyswitch Macro Pad with 2 rotary encoders and support for 6+ Layers of Macros.

---
## What is this?

This is a simple 9 key + 2 encoder macropad that runs on a Pi Pico. Total build cost is under $30 if you shop smart. The case is 3D Printed and held together with magnets allowing for easy assembly. 

There are 6 pages of macros availble to be set by the user.

Below will be a guide on how to install the software. Pinout is in the file named "pinout.md". 

---

### List of Required Hardware

- Raspberry Pi Pico with CircuitPython installed.
- 3D Printed case
- 8x 6mm*3mm magnets
- 0.96 Inch OLED Module (128x64)
- 9 mechanical switches
- 2 rotary encoders:
  - Rotary Encoder 1 (Volume Control)
  - Rotary Encoder 2 (Layer Selector)

 ---

# Printing/Case assembly

The case prints in two parts, top and bottom. I printed them in ASA but any material should be fine. 2-3 walls and 15-25% infill for both parts.

Glue the magnets in using superglue, ensure that polarity is correct.

The OLED can be glued in using hot glue or super glue as well

The Pico is held in with double sided 3M Tape.

I used knobs from here: https://www.printables.com/model/334111-encoder-knob Specifically the 20mm variant scaled up by 1mm

I used these keycaps: https://www.printables.com/model/118708-simple-cherry-mx-keycap

 
# Basic Script Install Guide

### List of Required Libraries

These are all included in the Lib Folder

- `adafruit_hid` for keyboard and consumer control functionalities.
- `adafruit_ssd1306` for OLED display control.
- `busio` for I2C and other bus communications.
- `digitalio` for digital input and output.
- `rotaryio` for rotary encoder input.
- `usb_hid` for USB Human Interface Device communication.
- `time` for handling time-related functions.

---

#### Installing CircuitPython on Raspberry Pi Pico:

1. **Download CircuitPython for Pico**: Visit the [CircuitPython Download Page for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/) and download the latest `.uf2` file.

2. **Enter Bootloader Mode**: Connect the Pico to your computer while holding down the BOOTSEL button. The Pico will appear as a USB drive.

3. **Flash CircuitPython**: Drag the downloaded `.uf2` file onto the Pico's USB drive. The Pico will reboot as a `CIRCUITPY` drive.

#### Installing Required Libraries:

1. **Download Libraries**: Download the Lib zip files from this Repo and extract it

2. **Copy Required Libraries to Pico**:
   - Connect your Pico to your computer.
   - Open the `CIRCUITPY` drive.
   - Copy the entire `lib` folder from the extracted bundle to the `CIRCUITPY` drive.

---

#### Installing the Script:

1. **Prepare the Code**: Download the 'code.py' file from this repo. Ensure that it is named `code.py`.

2. **Copy the Code to Pico**:
   - Connect the Pico to your computer.
   - Drag and drop or copy-paste the `code.py` file onto the `CIRCUITPY` drive.

3. **Safely Eject Pico**: After copying the files, safely eject the Pico from your computer.

4. **Test the Setup**: The Pico will run `code.py` automatically when powered up or reset.

---

#### Troubleshooting:

- If the OLED display or switches don't work as expected, check the hardware connections.
- For errors, connect to the Pico's serial console to view error messages.
- Ensure all libraries are compatible with your CircuitPython version.


---


# Script modification:

### Modifying Macros

Your macros are defined in the `layers` array. Each layer is a list of `Keycode` values from the `adafruit_hid.keycode` library, representing different keyboard keys or combinations.

#### Example: Changing Macros

Suppose you want to change the first key in Layer 1 to be the "Enter" key. You'll locate the first list in the `layers` array and replace `Keycode.A` with `Keycode.ENTER`.

Before:
```python
layers = [
    [Keycode.A, Keycode.B, Keycode.C, ...],
    ...
]
```

After:
```python
layers = [
    [Keycode.ENTER, Keycode.B, Keycode.C, ...],
    ...
]
```

#### Adding a New Layer

To add a new layer, you'll append a new list to the `layers` array. For example, adding a layer with various multimedia keys:

```python
layers = [
    ...,
    [Keycode.PLAY_PAUSE, Keycode.VOLUME_UP, Keycode.VOLUME_DOWN, ...]
]
```

### Updating the Screen Display

The function `keycode_to_string` translates `Keycode` values to a string representation for the display. You need to update this function if you add keycodes that are not already mapped.

#### Example: Adding a Display Name for a New Keycode

If you added `Keycode.PLAY_PAUSE`, but it's not in `keycode_to_string`, add it like this:

Before:
```python
def keycode_to_string(keycode):
    keycode_dict = {
        Keycode.A: "A",
        Keycode.B: "B",
        ...
    }
    return keycode_dict.get(keycode, "Unknown Key")
```

After:
```python
def keycode_to_string(keycode):
    keycode_dict = {
        Keycode.A: "A",
        Keycode.B: "B",
        Keycode.PLAY_PAUSE: "Play/Pause",
        ...
    }
    return keycode_dict.get(keycode, "Unknown Key")
```

### Practical Examples

#### Example 1: Adding a Layer for Media Controls

1. **Add New Layer**: Add a new layer for media controls.

    ```python
    layers = [
        ...,
        [Keycode.PLAY_PAUSE, Keycode.VOLUME_UP, Keycode.VOLUME_DOWN, Keycode.MUTE, ...]
    ]
    ```

2. **Update `keycode_to_string`**: Add new entries for media keys.

    ```python
    def keycode_to_string(keycode):
        keycode_dict = {
            ...,
            Keycode.PLAY_PAUSE: "Play",
            Keycode.VOLUME_UP: "Vol+",
            Keycode.VOLUME_DOWN: "Vol-",
            Keycode.MUTE: "Mute",
            ...
        }
        return keycode_dict.get(keycode, "Unknown Key")
    ```

#### Example 2: Custom Macro Layer

1. **Add Custom Layer**: Suppose you want a layer for specific functions or shortcuts.

    ```python
    layers = [
        ...,
        [Keycode.COPY, Keycode.PASTE, Keycode.CUT, ...]
    ]

    ```

2. **Update `keycode_to_string`**: Add new entries for these functions.

    ```python
    def keycode_to_string(keycode):
        keycode_dict = {
            ...,
            Keycode.COPY: "Copy",
            Keycode.PASTE: "Paste",
            Keycode.CUT: "Cut",
            ...
        }
        return keycode_dict.get(keycode, "Unknown Key")
    ```

### Important Notes

- When adding new keycodes, ensure they are supported by the `adafruit_hid` library.
- Test your changes carefully, especially if combining multiple keys into a macro.
- Updating the display to match your macros helps keep track of each button's function, especially as you switch between layers.

By following these guidelines, you can customize the macros and display information on your macropad to suit your specific needs.
