"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/i2c*  ou /dev/i2c-*

https://pypi.org/project/oled-text/

pip install oled-text

Pinos ttyS0
-I2C0_SCLK: Header 17 - GPIOC27
-I2C0_DATA: Header 19 - GPIOC26
"""


from periphery import I2C
from oled_text import OledText

# Open i2c-0 controller
i2c = I2C("/dev/i2c-0")


# Create the display, pass its pixel dimensions
oled = OledText(i2c, 128, 64)

# Write to the oled
oled.text("Hello ...", 1)  # Line 1
oled.text("... world!", 2)  # Line 2

i2c.close()


