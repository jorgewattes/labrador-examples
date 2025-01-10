# Memory-Mapped I/O

"""
# Endereços de Periféricos da Labrador (Caninos Loucos)

## Real-Time Clock (RTC)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E3E000     | Base do RTC                     | Subsistema RTC (Real-Time Clock)                              | Registro base                         |
| 0x44E3E000 + 0x00 | Registro de Segundos          | Armazena os segundos atuais                                   | 0-59                                  |
| 0x44E3E000 + 0x04 | Registro de Minutos           | Armazena os minutos atuais                                    | 0-59                                  |
| 0x44E3E000 + 0x08 | Registro de Horas             | Armazena as horas atuais                                      | 0-23                                  |

## Módulo de Controle (Control Module)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E10000     | Base do Módulo de Controle      | Controla várias funcionalidades do SoC                        | Registro base                         |
| 0x44E10000 + 0x630 | MAC ID0 (parte inferior)      | Bits inferiores do endereço MAC                               | Inteiros                              |
| 0x44E10000 + 0x634 | MAC ID0 (parte superior)      | Bits superiores do endereço MAC                               | Inteiros                              |

## GPIO (General Purpose Input/Output)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x4804C000     | GPIO1 Base                      | Controla o GPIO1                                              | Bits de configuração                  |
| 0x481AC000     | GPIO2 Base                      | Controla o GPIO2                                              | Bits de configuração                  |
| 0x481AE000     | GPIO3 Base                      | Controla o GPIO3                                              | Bits de configuração                  |

## UART (Universal Asynchronous Receiver-Transmitter)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x4806A000     | UART0 Base                      | Comunicação serial UART0                                      | Registro base                         |
| 0x4816C000     | UART1 Base                      | Comunicação serial UART1                                      | Registro base                         |

## SPI (Serial Peripheral Interface)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x48030000     | SPI0 Base                       | Configuração do barramento SPI0                               | Bits de configuração                  |
| 0x481A0000     | SPI1 Base                       | Configuração do barramento SPI1                               | Bits de configuração                  |

## I2C (Inter-Integrated Circuit)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E0B000     | I2C0 Base                       | Barramento I2C0 para comunicação com periféricos              | Bits de configuração                  |
| 0x4802A000     | I2C1 Base                       | Barramento I2C1                                               | Bits de configuração                  |

## PWM (Pulse-Width Modulation)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x48300000     | PWM Subsystem                   | Configuração de canais PWM                                    | Bits de duty cycle e frequência       |

## ADC (Analog-to-Digital Converter)
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E0D000     | ADC Base                        | Subsistema de conversão analógica para digital                | Valores de 12 bits                    |

## Clocks
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E00400     | Clock Manager                   | Configuração de fontes e divisores de clock                   | Bits de configuração                  |

## Watchdog
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x44E35000     | Watchdog Timer                  | Configuração do watchdog para reinicialização automática       | Bits de timeout                       |

## SRAM e Flash
| Endereço       | Função                           | Descrição                                                     | Valores Possíveis                     |
|----------------|----------------------------------|---------------------------------------------------------------|---------------------------------------|
| 0x40200000     | SRAM Base                       | Memória RAM do SoC                                            | Dados variáveis                       |
| 0x08000000     | Flash Base                      | Memória Flash externa                                         | Dados variáveis                       |

# Observações
- Certifique-se de consultar o **datasheet do AM335x** para detalhes completos sobre os registros e suas configurações.
- Alterar valores incorretamente pode causar falhas no sistema.
"""

from periphery import MMIO
import time
import os, sys
if os.geteuid() != 0:
    os.execvp('sudo', ['sudo', 'python3'] + sys.argv)


rtc_mmio = MMIO(0x44E3E000, 0x1000)
rtc_secs = rtc_mmio.read32(0x00)    #Offset do registro de segundos.
rtc_mins = rtc_mmio.read32(0x04)    #Offset do registro de minutos.
rtc_hrs = rtc_mmio.read32(0x08)     #Offset do registro de horas.
print("hours: {:02x} minutes: {:02x} seconds: {:02x}".format(rtc_hrs, rtc_mins, rtc_secs))

time.sleep(3) # delay de 3 segundos

rtc_secs = rtc_mmio.read32(0x00)    #Offset do registro de segundos.
rtc_mins = rtc_mmio.read32(0x04)    #Offset do registro de minutos.
rtc_hrs = rtc_mmio.read32(0x08)     #Offset do registro de horas.
print("hours: {:02x} minutes: {:02x} seconds: {:02x}".format(rtc_hrs, rtc_mins, rtc_secs))

rtc_mmio.close()
