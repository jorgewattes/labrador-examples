"""

Antes de executar este script, execute os seguintes comandos para ter acesso aos gpiochips

$ sudo chown caninos /dev/gpiochip*
$ sudo chmod g+rw /dev/gpiochip*
 
"""
#/dev/gpiochip0 - A
#/dev/gpiochip1 - B
#/dev/gpiochip2 - C
#/dev/gpiochip3 - D
#/dev/gpiochip4 - E

from periphery import GPIO
import time

# Configura a variável LED - como na GPIO /dev/gpiochip4 (E) linha 2 como saída - GPIO-E2 (Header-5)
led = GPIO("/dev/gpiochip4", 2, "out") # 
while True:
    led.write(True) 
    time.sleep(1) 
    led.write(False) 
    time.sleep(1) 


