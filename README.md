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
- 0.96 Inch OLED Module (128x64)
- 9 mechanical switches
- 2 rotary encoders:
  - Rotary Encoder 1 (Volume Control)
  - Rotary Encoder 2 (Layer Selector)

 ---

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

### Basic Script Install Guide

#### Installing CircuitPython on Raspberry Pi Pico:

1. **Download CircuitPython for Pico**: Visit the [CircuitPython Download Page for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/) and download the latest `.uf2` file.

2. **Enter Bootloader Mode**: Connect the Pico to your computer while holding down the BOOTSEL button. The Pico will appear as a USB drive.

3. **Flash CircuitPython**: Drag the downloaded `.uf2` file onto the Pico's USB drive. The Pico will reboot as a `CIRCUITPY` drive.

#### Installing Required Libraries:

1. **Download Libraries**: Download the /Lib folder from this Repo.

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


### Script modification:
