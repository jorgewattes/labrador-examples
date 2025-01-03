import time
from periphery import PWM
from periphery import MMIO

# Open PWM chip 2, channel 1 - GPIO-A27 (header-5)
pwm = PWM(2, 1)
pwm.frequency = 1e3# Set frequency to 1 kHz
pwm.duty_cycle = 0.75# Set duty cycle to 75%
pwm.enable()

# Mapear a memória do ADC
ADC_BASE = 0x44E0D000
ADC_SIZE = 0x1000
adc_mmio = MMIO(ADC_BASE, ADC_SIZE)

# Configurar o ADC (habilitar e configurar tensão de referência)
adc_mmio.write32(0x04, 0x01)  # Configuração básica do ADC

# Selecionar canal AIN0
adc_mmio.write32(0x48, 0x00)  # Selecionar canal 0 (AIN0)

try:
    while(1):
        # Iniciar uma conversão e ler o valor
        adc_mmio.write32(0x50, 0x01)  # Configurar step para iniciar conversão
        adc_value = adc_mmio.read32(0x58) ;  # Ler o valor convertido do FIFO0

        # Imprimir o valor lido
        print("ADC Value AIN7 (4.096): ", adc_value)

        pwm.duty_cycle = adc_value /2**12 # Converte para %

        print("PWM Duty-Cicle (%): ", pwm.duty_cycle)
        time.sleep(1)

finally:
   # Fechar o mapeamento de memória
   adc_mmio.close()
   pwm.close()