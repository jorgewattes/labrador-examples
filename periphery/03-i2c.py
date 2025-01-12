"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/i2c*  ou /dev/i2c-*

Pinos ttyS0
-I2C0_SCLK: Header 17 - GPIOC27
-I2C0_DATA: Header 19 - GPIOC26

"""

from periphery import I2C
from oled_text import OledText

# Open i2c-0 controller
i2c = I2C("/dev/i2c-0")

# Read byte at address 0x100 of EEPROM at 0x50
msgs = [I2C.Message([0x01, 0x00]), I2C.Message([0x00], read=True)]
i2c.transfer(0x50, msgs)
print("0x100: 0x{:02x}".format(msgs[1].data[0]))


i2c.close()


