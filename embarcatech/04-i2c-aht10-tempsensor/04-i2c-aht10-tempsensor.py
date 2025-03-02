"""
Liste os dispositivos I2c no sistema para garantir que estão habilitados:

$ ls /dev/i2c*  ou /dev/i2c-*

Pinos ttyS0
-I2C0_SCLK: Header 08 - GPIOC27
-I2C0_DATA: Header 10 - GPIOC26

sudo chmod a+rw /dev/i2c-*

sudo apt-get install -y i2c-tools  # Instale a ferramenta, se necessário
i2cdetect -y 1  # Substitua "1" pelo número do barramento listado anteriormente

SSD1306
"""

from periphery import I2C
import time

# Configurações
I2C_BUS = "/dev/i2c-2"  # Substitua pelo seu barramento I²C
I2C_ADDRESS = 0x38      # Endereço do AHT10

# Inicialização do barramento I2C
i2c = I2C(I2C_BUS)

def aht10_read():
    """Lê temperatura e umidade do sensor AHT10."""
    # Envia comando para iniciar medição
    measure_command = [0xAC, 0x33, 0x00]
    i2c.transfer(I2C_ADDRESS, [I2C.Message(measure_command)])
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

def aht10_init():
    """Inicializa o sensor AHT10."""
    init_command = [0xE1, 0x08, 0x00]  # Comando para inicializar o AHT10
    i2c.transfer(I2C_ADDRESS, [I2C.Message(init_command)])  # Envia comando de inicialização
    time.sleep(0.02)  # Aguarde 20ms para estabilização

while True:
    aht10_init()  # Inicializa o sensor
    temp, hum = aht10_read()  # Lê os valores de temperatura e umidade
    print(f"Temperatura: {temp:.2f} °C, Umidade: {hum:.2f} %")

