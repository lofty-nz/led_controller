# LED Controller README

## Introduction
This is the repository for the LED Controller program. It uses a Raspberry Pi Pico W, a WS2812 LED strip, an EC11 encoder, and a potentiometer to create an interactive LED strip light display.

## Version
LED controller code v1.0

## Hardware Used
1. Raspberi Pi Pico W
2. WS2812 LED strip
3. EC11 Encoder
4. Potentiometer

## Libraries
The following libraries are used in this code:

- `machine` (for controlling the GPIO pins)
- `time` (for timing related functions)
- `neopixel` (for controlling the LED strip)
- `urandom` (for generating random numbers)
- `math` (for mathematical operations)
- `rotary_irq_rp2` (for controlling the rotary encoder)

## Software features
1. Control the brightness of the LED strip.
2. Cycle through different lighting patterns.
3. Interactive menu system to adjust settings and control patterns.
4. Automatic mode for rotating through patterns.
5. Control patterns via the EC11 encoder and button.

## How to use
1. Connect the hardware as described in the comments of the source code.
2. Run the Python script on your Raspberry Pi.
3. The LED strip will start displaying patterns.
4. Use the rotary encoder to navigate through the menu.
5. Press the rotary encoder's button to select an option in the menu.

## Animations
There are three animations available: rainbow, breathing, and transition.

## Future Work
Future updates will include more patterns, better user control, and the ability to save and load user settings.

## Disclaimer
This code is provided as-is, without any warranty or guarantee of functionality. Always ensure you are using the correct voltage for your LED strip to avoid damaging your hardware.