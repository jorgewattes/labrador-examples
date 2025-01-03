"""
# Tabela de Pinos PWM - Header da Labrador Caninos Loucos

| Chip      | Channel   | Pino Físico (Header) | Função PWM   | Observação                      |
|-----------|-----------|----------------------|--------------|---------------------------------|
| pwmchip0  | 0         | 8                   | GPIOB08/PWM3/SDO_CLK/KS_OUT1 | PWM associado ao PWMSS1         |
| pwmchip0  | 1         | 34                  | GPIOC22/TWI3_SCLK/PCM0_CLK/SPIO_SCLK | PWM associado ao PWMSS1         |
| pwmchip1  | 0         | 33                  | GPIOA28/PCM0_IN/I2S_BCLK0    | PWM associado ao PWMSS2         |
| pwmchip1  | 1         | 35                  | GPIOA31/I2S_D1               | PWM associado ao PWMSS2         |
| pwmchip2  | 0         | 37                  | GPIOA27/I2S_D0               | PWM associado ao PWMSS0         |
| pwmchip2  | 1         | 5                   | GPIOA27/I2S_D0               | PWM associado ao PWMSS0         |

## Descrição dos Campos
- **Chip**: Identifica o subsistema PWM no Linux, exposto como `pwmchipX`.
- **Channel**: Canal específico dentro do chip PWM (`0` ou `1`).
- **Pino Físico (Header)**: Pino físico no header da Labrador usado para o PWM.
- **Função PWM**: Nome da funcionalidade PWM associada ao pino no SoC.
- **Observação**: Indica o subsistema PWM (PWMSS) ao qual o pino pertence.

## Uso dos Pinos
- Certifique-se de configurar os pinos como PWM antes do uso. Exemplo para configurar o pino `8`:
    config-pin 8 pwm

## Exemplos de Código
1. Para ativar o PWM no channel 0 do pwmchip0:
    echo 0 > /sys/class/pwm/pwmchip0/export
    echo 20000000 > /sys/class/pwm/pwmchip0/pwm0/period  # Período de 20ms (50Hz)
    echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/duty_cycle  # Duty Cycle de 1ms
    echo 1 > /sys/class/pwm/pwmchip0/pwm0/enable

2. Para uso em Python com Python Periphery:
    from periphery import PWM
    pwm = PWM(chip=0, channel=0)
    pwm.frequency = 50  # 50 Hz
    pwm.duty_cycle = 0.05  # 5% Duty Cycle
    pwm.enable()
    pwm.disable()
    pwm.close()
"""


from periphery import PWM

# Open PWM chip 0, channel 10
pwm = PWM(0, 10)

# Set frequency to 1 kHz
pwm.frequency = 1e3
# Set duty cycle to 75%
pwm.duty_cycle = 0.75

pwm.enable()

# Change duty cycle to 50%
pwm.duty_cycle = 0.50

pwm.close()