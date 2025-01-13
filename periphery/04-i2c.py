"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/i2c*  ou /dev/i2c-*

Pinos ttyS0
-I2C0_SCLK: Header 08 - GPIOC27
-I2C0_DATA: Header 10 - GPIOC26


Instalar a biblioteca OledText
$ pip install oled-text

SSD1306
"""

# from periphery import I2C
# # from oled_text import OledText

# # Open i2c-0 controller
# i2c = I2C("/dev/i2c-0")

# # Read byte at address 0x100 of EEPROM at 0x78
# msgs = [I2C.Message([0x01, 0x00]), I2C.Message([0x00], read=True)]
# i2c.transfer(0x50, msgs)
# print("0x100: 0x{:02x}".format(msgs[1].data[0]))

# i2c.close()


# from periphery import I2C
# from oled_text import OledText

# # Open i2c-0 controller
# i2c = I2C("/dev/i2c-0")


# # Create the display, pass its pixel dimensions
# oled = OledText(i2c, 128, 64)

# # Write to the oled
# oled.text("Hello ...", 1)  # Line 1
# oled.text("... world!", 2)  # Line 2

# i2c.close()

from periphery import I2C
import time

# Configurações
I2C_BUS = "/dev/i2c-1"  # Substitua pelo seu barramento I²C
I2C_ADDRESS = 0x38      # Endereço do AHT10

# Inicialização do barramento I2C
i2c = I2C(I2C_BUS)

def aht10_init():
    """Inicializa o sensor AHT10."""
    init_command = [0xE1, 0x08, 0x00]  # Comando para inicializar o AHT10
    i2c.transfer(I2C_ADDRESS, [I2C.Message([0x00] + init_command)])  # Envia comando de inicialização
    time.sleep(0.02)  # Aguarde 20ms para estabilização

def aht10_read():
    """Lê temperatura e umidade do sensor AHT10."""
    # Envia comando para iniciar medição
    measure_command = [0xAC, 0x33, 0x00]
    i2c.transfer(I2C_ADDRESS, [I2C.Message([0x00] + measure_command)])
    time.sleep(0.08)  # Aguarde 80ms para conversão

    # Lê os 6 bytes de dados do sensor
    read_message = I2C.Message([0x00] * 6, read=True)
    i2c.transfer(I2C_ADDRESS, [read_message])
    data = read_message.data

    # Processa os dados retornados
    humidity_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
    temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

    # Calcula umidade e temperatura reais
    humidity = (humidity_raw / 1048576) * 100  # Em percentual
    temperature = (temperature_raw / 1048576) * 200 - 50  # Em °C

    return temperature, humidity

# Main
try:
    aht10_init()  # Inicializa o sensor
    temp, hum = aht10_read()  # Lê os valores de temperatura e umidade
    print(f"Temperatura: {temp:.2f} °C, Umidade: {hum:.2f} %")
finally:
    i2c.close()  # Fecha o barramento I2C
