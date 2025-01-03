from periphery import GPIO
import time

#GPIO-D17 - LED (BLUE)
#/dev/gpiochip0 - A
#/dev/gpiochip1 - B
#/dev/gpiochip2 - C
#/dev/gpiochip3 - D
#/dev/gpiochip4 - E

# Open LED - GPIO /dev/gpiochip0 line 17 with input direction
led = GPIO("/dev/gpiochip3", 17, "in") # GPIO-D17

# Open Button - GPIO /dev/gpiochip0 line 3 with output direction
button = GPIO("/dev/gpiochip4", 3, "out") # GPIO-E3 (Header-3)
# Set pull-up / pull-down internal resistor
button.bias("pull_up") 

try:
    while(1):
        
        if(not button.read()): # If button pressed:
            led.write(not led.read()) # Inverts LED Status
            time.sleep(0.3) # Delay to bounce filter
finally:
    button.close()
    led.close()

