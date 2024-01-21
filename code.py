import time
import board
import busio
import digitalio
import rotaryio
import adafruit_ssd1306
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# OLED display size
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Initialize I2C
i2c = busio.I2C(scl=board.GP19, sda=board.GP18)

# Initialize OLED display
oled_address = 0x3C  # or 0x3D if your display has a different address
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=oled_address)

# Initialize keyboard and consumer control
kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

# Define the GPIO pins for the switches
# Modify this list to match your physical layout
switch_pins = [board.GP6, board.GP7, board.GP8, 
               board.GP3, board.GP4, board.GP5, 
               board.GP0, board.GP1, board.GP2]
switches = [digitalio.DigitalInOut(pin) for pin in switch_pins]
for switch in switches:
    switch.direction = digitalio.Direction.INPUT
    switch.pull = digitalio.Pull.UP

# Define rotary encoders
# Modify this list to match your physical layout
rotary1 = rotaryio.IncrementalEncoder(board.GP15, board.GP14)
rotary2 = rotaryio.IncrementalEncoder(board.GP10, board.GP11)
button1 = digitalio.DigitalInOut(board.GP13)
button2 = digitalio.DigitalInOut(board.GP9)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

# Layers and macros
# This is where you define the layers and what each button press will do.
# Remove/add layers if needed 
layers = [
    # Layer 1
    [Keycode.A, Keycode.B, Keycode.C, Keycode.D, Keycode.E, Keycode.F, Keycode.G, Keycode.H, Keycode.I],
    # Layer 2
    [Keycode.J, Keycode.K, Keycode.L, Keycode.M, Keycode.N, Keycode.O, Keycode.P, Keycode.Q, Keycode.R],
    # Layer 3
    [Keycode.S, Keycode.T, Keycode.U, Keycode.V, Keycode.W, Keycode.X, Keycode.Y, Keycode.Z, Keycode.ONE],
    # Layer 4
    [Keycode.TWO, Keycode.THREE, Keycode.FOUR, Keycode.FIVE, Keycode.SIX, Keycode.SEVEN, Keycode.EIGHT, Keycode.NINE, Keycode.ZERO],
    # Layer 5
    [Keycode.F1, Keycode.F2, Keycode.F3, Keycode.F4, Keycode.F5, Keycode.F6, Keycode.F7, Keycode.F8, Keycode.F9],
    # Layer 6
    [Keycode.F10, Keycode.F11, Keycode.F12, Keycode.ESCAPE, Keycode.TAB, Keycode.CAPS_LOCK, Keycode.SHIFT, Keycode.CONTROL, Keycode.ALT]
]

current_layer = 0
selected_layer = 0
last_position_layer = 0
last_position_volume = 0  # Initialize last_position_volume

def underline_text(oled, text, x, y, underline):
    oled.text(text, x, y, 1)
    if underline:
        for i in range(len(text)):
            oled.pixel(x + i * 6, y + 10, 1)

# Mapping function for Keycode to string
# Defines what the keycode listed in layers, displays as on the OLED.
# The keycode and displayed value dont have to match. ie "Pause" can be displayed for "Keycode.F1"
def keycode_to_string(keycode):
    keycode_dict = {
        Keycode.A: "A", Keycode.B: "B", Keycode.C: "C", Keycode.D: "D",
        Keycode.E: "E", Keycode.F: "F", Keycode.G: "G", Keycode.H: "H",
        Keycode.I: "I", Keycode.J: "J", Keycode.K: "K", Keycode.L: "L",
        Keycode.M: "M", Keycode.N: "N", Keycode.O: "O", Keycode.P: "P",
        Keycode.Q: "Q", Keycode.R: "R",
        Keycode.S: "S", Keycode.T: "T", Keycode.U: "U", Keycode.V: "V",
        Keycode.W: "W", Keycode.X: "X", Keycode.Y: "Y", Keycode.Z: "Z",
        Keycode.ONE: "1", Keycode.TWO: "2", Keycode.THREE: "3", 
        Keycode.FOUR: "4", Keycode.FIVE: "5", Keycode.SIX: "6", 
        Keycode.SEVEN: "7", Keycode.EIGHT: "8", Keycode.NINE: "9",
        Keycode.ZERO: "0", Keycode.F1: "F1", Keycode.F2: "F2", 
        Keycode.F3: "F3", Keycode.F4: "F4", Keycode.F5: "F5",
        Keycode.F6: "F6", Keycode.F7: "F7", Keycode.F8: "F8", 
        Keycode.F9: "F9", Keycode.F10: "F10", Keycode.F11: "F11",
        Keycode.F12: "F12", Keycode.ESCAPE: "ESC", Keycode.TAB: "TAB",
        Keycode.CAPS_LOCK: "CAPS", Keycode.SHIFT: "SHIFT", 
        Keycode.CONTROL: "CTRL", Keycode.ALT: "ALT"
    }
    return keycode_dict.get(keycode, "Unknown Key")

# Update the display
def update_display():
    oled.fill(0)
    for layer_index in range(len(layers)):
        underline_text(oled, f"L{layer_index + 1}", layer_index * 20, 0, selected_layer == layer_index)

    header_height = 20  # Space occupied by the header
    total_rows = 4     # Total number of rows needed for keycodes
    available_height = OLED_HEIGHT - header_height  # Height available for keycodes
    row_height = available_height // total_rows  # Height for each row

    for i, keycode in enumerate(layers[current_layer]):
        x = (i % 3) * 40
        y = (i // 3) * row_height + header_height  # Calculate y position

        oled.text(keycode_to_string(keycode), x, y, 1)

    oled.show()

update_display()

while True:
    # Check layer selection rotary encoder
    position_layer = rotary2.position
    new_selected_layer = position_layer % len(layers)
    if new_selected_layer != selected_layer:
        selected_layer = new_selected_layer
        update_display()

    # Check if rotary encoder button is pressed
    if not button2.value:
        current_layer = selected_layer
        update_display()
        time.sleep(0.2)  # Debounce delay

    # Handle volume control
    position_volume = rotary1.position
    if position_volume > last_position_volume:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif position_volume < last_position_volume:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_position_volume = position_volume

    if not button1.value:
        cc.send(ConsumerControlCode.MUTE)  # Mute/unmute
        time.sleep(0.2)  # Debounce delay

    # Check switches and send corresponding macros
    for i, switch in enumerate(switches):
        if not switch.value:
            kbd.send(layers[current_layer][i])
            while not switch.value:
                pass  # Wait for switch release

    time.sleep(0.1)