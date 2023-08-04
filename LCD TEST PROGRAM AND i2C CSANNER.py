#I2C scanner and 1602 LCD display driver
#tutorial page: https://github.com/gigafide/pico_LCD_16x2
#tutorial vid: https://www.youtube.com/watch?v=B8Kr_3xHjqE&ab_channel=Tinkernut
import utime
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd #library:  https://github.com/T-622/RPI-PICO-I2C-LCD
I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
loop_count = 0
i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000) #SDA pin6 green / SCL pin7 yellow
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
device_addresses = i2c.scan()

if device_addresses: # Check if any addresses were found
    first_device_address = device_addresses[0]
    print('I2C addy (raw) =', first_device_address)
    print('I2C addy (hex) =', hex(first_device_address))
else:
    print('No devices found')

def loop():
    global loop_count
    loop_count += 1
    print(loop_count)
    lcd.clear()
    lcd.move_to(0,0) #(x,y)
    lcd.putstr("Howdy")
    lcd.move_to(1,1)
    lcd.putstr("Tinkernerdz!")
    utime.sleep(0.25)
    
while True:  # This will cause the loop to run forever.
    loop()