#LED controller code v1.0
#Hardware used, Raspberi Pi Pico W, WS2812 LED strip, EC11 Encoder, Potentiometer
# made this change to test github
# changes commited
# import libraries
from machine import ADC, Pin
import time
import machine
import neopixel
import urandom
import math
from rotary_irq_rp2 import RotaryIRQ

# Define constants
FRAMES_PER_SECOND = 120
adc = ADC(Pin(28))
NUM_LEDS = 32 # Set the number of LEDs in your strip
MAX_BRIGHTNESS = 7
MIN_BRIGHTNESS = 25
FRAMES_PER_SECOND = 120
button = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)# Setup the Encoder Button
led_pin = machine.Pin(16)# Set up the neopixel object for controlling the LEDs
np = neopixel.NeoPixel(led_pin, NUM_LEDS)
encoderpin1 = 0
encoderpin2 = 1
 
# Global Variables
brightness = 7  # Add a global variable for brightness
gCurrentPatternNumber = 0  # Index number of the current pattern
gHue = 0  # Rotating "base color" used by many of the patterns
current_pattern = None  # Current pattern name
pattern_start = True  # Flag to track if a pattern has just started
loop_count = 0
automode = True
staticHue = 0 # Add a global variable for staticHue
# Additional global variables for menu
current_val = 0
button_pressed = False
button_previous = False
last_interaction_time = time.ticks_ms()
menu_mode = False # Add a global variable for menu mode
menu_position = 0 # Menu position
pattern1_enabled = True
pattern2_enabled = True
pattern3_enabled = True
menu_select_mode = False # Add a global variable for menu select mode
menu = ["Toggle Automode", "Adjust brightness", "Advance pattern", "Toggle animation 1 on/off", "Toggle animation 2", "Toggle animation 3"]


def update_menu_values():
    global menu_values, automode, brightness, gCurrentPatternNumber, pattern1_enabled, pattern2_enabled, pattern3_enabled
    menu_values = [automode, brightness, gCurrentPatternNumber, pattern1_enabled, pattern2_enabled, pattern3_enabled]

rotary = RotaryIRQ(encoderpin1, encoderpin2)
#current_val = 0  # Track the last known value of the encoder
new_poll_value = 0
previous_value = 0
# Additional global variables for menu
button_pressed = False
button_previous = False

# Global Variables
last_button_press_ms = 0 # Add this new global variable

# Button press handler activated by interrupt
def button_press(pin):
    global menu_mode, last_interaction_time, menu_select_mode, last_button_press_ms

    # Ignore button presses that happen too close together (within 200 ms of each other)
    current_ms = time.ticks_ms()
    if time.ticks_diff(current_ms, last_button_press_ms) < 200:
        return
    last_button_press_ms = current_ms

    if not menu_mode and not menu_select_mode:  # Not in menu mode and not in menu select mode
        menu_mode = True  # Enter menu mode
        print(f'76 Encoder clicked, entering menu mode, current position: {menu[menu_position]}')  # Debug print

    elif menu_mode and not menu_select_mode:  # In menu mode, but not in menu select mode
        menu_select_mode = True  # Enter menu select mode
        print(f'80 Encoder clicked, edit {menu[menu_position]} setting current value is : {automode}')  # Debug print

    elif menu_mode and menu_select_mode:  # In menu mode and in menu select mode
        print(f'83 Encoder clicked, editing {menu[menu_position]} setting, current value: {automode}')  # Debug print
        menu_mode = False  # Exit menu mode
        print('Exiting menu system')  # Debug print

    last_interaction_time = time.ticks_ms()  # Reset timer to prevent menu from timing out

# Attach interrupt to button
button.irq(trigger=machine.Pin.IRQ_RISING, handler=button_press)

# Function to update the 'menu_values' list, which stores the current values of 
# various settings that the user can modify through the menu.
def update_menu_values():
    # We need to access these global variables because they represent the state of
    # various settings (e.g., automode, brightness, pattern number, pattern enabling).
    global menu_values, automode, brightness, gCurrentPatternNumber, pattern1_enabled, pattern2_enabled, pattern3_enabled
    # We update the 'menu_values' list with the current values of the variables.
    # These variables may have been modified elsewhere in the code (e.g., through the menu system).
    # Updating the 'menu_values' list ensures that it accurately reflects the current state of these variables.
    menu_values = [automode, brightness, gCurrentPatternNumber, pattern1_enabled, pattern2_enabled, pattern3_enabled]
    # Now, 'menu_values' has been updated with the current state of the settings.
    # If the menu system tries to display the current value of a setting (e.g., brightness),
    # it will now display the correct, current value.
    
# Function to poll the rotary encoder for its current value
def poll_encoder():
    global current_val, button_pressed, button_previous, last_interaction_time, new_poll_value
    try:
        new_poll_value = rotary.value()
        
        if current_val != new_poll_value:
           # print('Encoder (current)value changed from', current_val, 'to', new_poll_value)
            current_val = new_poll_value
            last_interaction_time = time.ticks_ms()
#             if time.ticks_diff(time.ticks_ms(), last_interaction_time) >= 2000:
#                 menu_mode = False
#                 menu_select_mode = False
        #print('Encoder being polled now, new poll value', new_poll_value) 
        return new_poll_value
    except Exception as e:
        print(f"Exception occurred: {e}")
        
def enter_menu():
    global menu_mode, menu_position, menu_select_mode, button_pressed, automode, brightness, new_val
    global pattern1_enabled, pattern2_enabled, pattern3_enabled, last_interaction_time, current_val
    global previous_value
    time.sleep(0.5)
    previous_val = current_val 
    menu_mode = True  
    prev_menu_position = menu_position
3.5.55....5
    while menu_mode:
        new_poll_value = poll_encoder()

        if new_poll_value > previous_val:  # Positive rotation
            if not menu_select_mode:  # Not in select mode, rotary encoder will change menu position
                menu_position = (menu_position + 1) % len(menu)
            elif menu_position == 0:  # Toggle automode
                print(f" 142 Turn Automode to {not automode}")  # Print the opposite value of automode before changing it
                automode = not automode  # Toggle automode
                print(f"144 Turn Automode to {not automode}")  # Print the opposite value of automode after changing it
                last_interaction_time = time.ticks_ms()

        elif new_poll_value < previous_val:  # Negative rotation
            if not menu_select_mode:  # Not in select mode, rotary encoder will change menu position
                menu_position = (menu_position - 1) % len(menu)
            elif menu_position == 0:  # Toggle automode
                automode = not automode  # Toggle automode
                last_interaction_time = time.ticks_ms()

        update_menu_values()  # Update menu_values list after a change

        # Print current menu position and its value
        if menu_select_mode and menu_position == 1:  # If in select mode and position is for brightness
            print(f"160 set brightness - {menu_values[menu_position]}")
        elif menu_position == 2:  # If the menu position is for 'advance pattern'
            print(f"162 {menu[menu_position]} - {patterns[gCurrentPatternNumber].__name__}")
        else:
            print(f"164 {menu[menu_position]} - {menu_values[menu_position]}")

        previous_val = current_val  # Update previous_val at the end of each loop iteration
        current_val = new_poll_value  # Update the current_val after the checks are done

        if time.ticks_diff(time.ticks_ms(), last_interaction_time) >= 5000:
            print('169 No interaction for 1 seconds, exiting menu')
            menu_mode = False

    print('Exited menu')
    menu_mode = False
    button_pressed = False


# ...
#######Animations #######

def rainbow(): # rainbow animation
    ##add code here to goto call next pattern if this pattern has been disabled
    for i in range(NUM_LEDS):
        np[i] = scale_color(wheel((int(i * 256 / NUM_LEDS) + gHue) & 255), brightness)

def breathing(): # breathing animation
    ##add code here to goto call next pattern if this pattern has been disabled
    t = time.ticks_ms() / 1000  # get current time in seconds
    # Generate brightness from sine wave that oscillates between 0 and 255
    raw_brightness = int((math.sin(t) + 1) / 2 * 255)
    # Scale the raw_brightness according to the ADC read brightness
    scaled_brightness = int(raw_brightness * brightness / 255)
    # Set the color to red by default unless the encoder is turned
    if staticHue == 0:
        color = (200, 200, 0)
    else:
        color = wheel(staticHue)
    # Scale color based on the scaled_brightness
    color = tuple(int(c * scaled_brightness / 255) for c in color)
    # Apply color to all LEDs
    np.fill(color)
    
def transition(): # transition animation
    ##add code here to goto call next pattern if this pattern has been disabled
    # Calculate the two end colors
    color1 = wheel(gHue)
    color2 = wheel((gHue + 128) % 256)
    # Set each LED to a color that's a blend of color1 and color2
    for i in range(NUM_LEDS):
        # Calculate the blend factor
        blend_factor = i / (NUM_LEDS - 1)
        # Blend the two colors
        blended_color = [int(color1[j] * (1 - blend_factor) + color2[j] * blend_factor) for j in range(3)]
        # Apply the color to the LED
        np[i] = scale_color(blended_color, brightness)  # Pass brightness as an argument here
       
######Animation helper functions######
  
# Helper function to scale color values based on brightness
def scale_color(color, brightness):
    return tuple(int(c * brightness / 255) for c in color)

def wheel(pos): # FastLED's built-in rainbow generator
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# ColorFromPalette function to get colors from a palette
def ColorFromPalette(palette, index, brightness=255):
    index = int(index)
    if index < len(palette):
        color = palette[index]
        return scale_color(color)
    return (0, 0, 0)

######Main program loop control######
last_pattern_change_ms = time.ticks_ms()
def loop():
    global last_pattern_change_ms, pattern_start
    global current_pattern
    global loop_count

    while True:
        loop_count += 1 #count loops to monitor interpreter performance
        patterns[gCurrentPatternNumber]() # Call the current pattern function once, updating the LEDs array
        np.write() #send array to led strip
        #print(f'Checking menu mode: {menu_mode}')  # Add this print statement
        if menu_mode == True or menu_select_mode == True:
            enter_menu()
              # If the pattern has just started, print the current pattern and reset the flag
        if pattern_start:
            current_pattern = patterns[gCurrentPatternNumber].__name__
            if menu_mode == False:
                print(f"257 Current Pattern: {current_pattern}")
            pattern_start = False  # Reset the flag

        # Do some periodic updates
        global gHue
        gHue = (gHue + 1) % 256

    if automode and time.ticks_diff(time.ticks_ms(), last_pattern_change_ms) >= 10000:
        last_pattern_change_ms = time.ticks_ms()  # Update the last change timestamp
        next_pattern()
            
def next_pattern():
    global gCurrentPatternNumber, pattern_start
    gCurrentPatternNumber = (gCurrentPatternNumber + 1) % len(patterns)
    pattern_start = True  # Set flag to True when the pattern changes
    
# List of patterns to cycle through
patterns = [transition, breathing,  rainbow]
gCurrentPatternNumber = 0  # Index number of the current pattern
gHue = 0  # Rotating "base color" used by many of the patterns
# Run the loop functions
loop() 
