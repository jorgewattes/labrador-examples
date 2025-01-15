"""
Para ativar o PWM no channel 0 do pwmchip0:
    echo 0 > /sys/class/pwm/pwmchip0/export
    echo 2000000000 > /sys/class/pwm/pwmchip0/pwm0/period  # Período de 20ms (50Hz)
    echo 1000000000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle  # Duty Cycle de 1ms
    echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

$ sudo chown caninos /dev/gpiochip*
$ sudo chmod g+rw /dev/gpiochip*
"""

import os
import time
from periphery import PWM

# Função para exportar o canal PWM automaticamente
def export_pwm(chip, channel):
    export_path = f"/sys/class/pwm/pwmchip{chip}/export"
    pwm_path = f"/sys/class/pwm/pwmchip{chip}/pwm{channel}"

    # Verifica se o canal já está exportado
    if not os.path.exists(pwm_path):
        try:
            with open(export_path, "w") as f:
                f.write(str(channel))
            print(f"Canal {channel} do chip {chip} exportado com sucesso.")
        except PermissionError:
            raise PermissionError("Permissões insuficientes para exportar o PWM. Execute como root ou ajuste as permissões.")

# Exporta e inicializa o PWM no chip 0, canal 0
chip = 0
channel = 0
export_pwm(chip, channel)

# Inicializa o PWM com a biblioteca periphery
pwm = PWM(chip, channel)
pwm.period = 0.02  # 20 ms (50 Hz)
pwm.duty_cycle = 0.05  # 5% duty cycle
pwm.enable()

inc = True

try:
    while True:
        # Incrementa ou decrementa o duty cycle
        if inc:
            pwm.duty_cycle = min(pwm.duty_cycle + 0.10, 1.0)  # Limita a 100%
            inc = False if pwm.duty_cycle >= 1.0 else True
        else:
            pwm.duty_cycle = max(pwm.duty_cycle - 0.10, 0.0)  # Limita a 0%
            inc = True if pwm.duty_cycle <= 0.0 else False

        # Espera antes de alterar o ciclo
        time.sleep(1)

except KeyboardInterrupt:
    # Garante que o PWM seja desativado ao sair
    pwm.disable()
    pwm.close()