"""

Antes de executar este script, execute os seguintes comandos para ter acesso aos gpiochips

$ sudo chown caninos /dev/gpiochip*
$ sudo chmod g+rw /dev/gpiochip*
 
"""

from periphery import GPIO
import time

#/dev/gpiochip0 - A
#/dev/gpiochip1 - B
#/dev/gpiochip2 - C
#/dev/gpiochip3 - D
#/dev/gpiochip4 - E

# Open LED - GPIO /dev/gpiochip0 line 17 with input direction
led = GPIO("/dev/gpiochip4", 2, "out") # GPIO-E2 (Header-5)

while True:
    led.write(True) 
    time.sleep(1) 
    led.write(False) 
    time.sleep(1) 


