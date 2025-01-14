"""
Para ativar o PWM no channel 0 do pwmchip0:
    echo 0 > /sys/class/pwm/pwmchip0/export
    echo 20000000 > /sys/class/pwm/pwmchip0/pwm0/period  # Período de 20ms (50Hz)
    echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle  # Duty Cycle de 1ms
    echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

"""

import time
from periphery import PWM


# Open PWM chip 2, channel 1 - GPIO-A27 (header-5)
#pwm = PWM(2, 1)

# Open PWM chip 1, channel 8 - GPIO-B8 (header-12)
pwm = PWM(0,0) 
pwm.frequency = 1e3 # Set frequency to 1 kHz
pwm.duty_cycle = 0.75 # Set duty cycle to 75%
pwm.enable()

inc=True

try:
    while(1):
        if(inc):
            pwm.duty_cycle = pwm.duty_cycle + 0.10
            inc=False if pwm.duty_cycle>=1 else True
        else:
            pwm.duty_cycle = pwm.duty_cycle - 0.10
            inc=True if pwm.duty_cycle<=0 else False
        time.sleep(1)
finally:
    pwm.close()