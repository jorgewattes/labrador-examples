"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/i2c*  ou /dev/i2c-*

Pinos ttyS0
-I2C0_SCLK: Header 08 - GPIOC27
-I2C0_DATA: Header 10 - GPIOC26

sudo chmod a+rw /dev/i2c-*

sudo apt-get install -y i2c-tools  # Instale a ferramenta, se necessário
i2cdetect -y 1  # Substitua "1" pelo número do barramento listado anteriormente

SSD1306
"""

# from periphery import I2C
# # from oled_text import OledText

# # Open i2c-0 controller
# i2c = I2C("/dev/i2c-2")

# # Read byte at address 0x100 of EEPROM at 0x78
# msgs = [I2C.Message([0x01, 0x00]), I2C.Message([0x00], read=True)]
# i2c.transfer(0x50, msgs)
# print("0x100: 0x{:02x}".format(msgs[1].data[0]))

# i2c.close()


from periphery import I2C

# Endereço I2C do display SSD1306
I2C_ADDRESS = 0x3C

# Configuração do barramento I2C (substitua "/dev/i2c-1" pelo seu barramento I2C)
i2c = I2C("/dev/i2c-1")

# Inicialização do SSD1306
def ssd1306_init():
    commands = [
        0xAE,  # Display OFF
        0xD5, 0x80,  # Set Display Clock Divide Ratio/Oscillator Frequency
        0xA8, 0x3F,  # Set Multiplex Ratio (1/64)
        0xD3, 0x00,  # Set Display Offset
        0x40,  # Set Display Start Line
        0x8D, 0x14,  # Charge Pump Setting (Enable)
        0x20, 0x00,  # Set Memory Addressing Mode (Horizontal Addressing)
        0xA1,  # Set Segment Re-map (Column Address 127 is mapped to SEG0)
        0xC8,  # Set COM Output Scan Direction (Remapped)
        0xDA, 0x12,  # Set COM Pins Hardware Configuration
        0x81, 0xCF,  # Set Contrast Control
        0xD9, 0xF1,  # Set Pre-charge Period
        0xDB, 0x40,  # Set VCOMH Deselect Level
        0xA4,  # Entire Display ON (Resume to RAM Content Display)
        0xA6,  # Set Normal Display (A6=Normal, A7=Inverse)
        0x2E,  # Deactivate Scroll
        0xAF   # Display ON
    ]
    for cmd in commands:
        i2c.transfer(I2C_ADDRESS, [I2C.Message([0x00, cmd])])  # Envia comando ao display

# Escreve "Hello, World!" no display
def ssd1306_draw_text(text):
    # Limpar o display
    buffer = [0x40] + [0x00] * 1024  # Display 128x64
    i2c.transfer(I2C_ADDRESS, [I2C.Message(buffer)])

    # Dados para escrever "Hello, World!" (substitua por uma função de desenho mais completa se necessário)
    hello_world = [
        0x40,  # Indica dados de memória gráfica
        # Adicione aqui os bytes que formam "Hello, World!" em uma fonte pequena
        # Exemplos de bytes podem ser gerados usando ferramentas externas ou bibliotecas específicas
    ]
    i2c.transfer(I2C_ADDRESS, [I2C.Message(hello_world)])

# Execução
try:
    ssd1306_init()
    ssd1306_draw_text("Hello, World!")
finally:
    i2c.close()


# from periphery import I2C
# import time

# # Configurações
# I2C_BUS = "/dev/i2c-2"  # Substitua pelo seu barramento I²C
# I2C_ADDRESS = 0x38      # Endereço do AHT10

# # Inicialização do barramento I2C
# i2c = I2C(I2C_BUS)
# I2C

# def aht10_init():
#     """Inicializa o sensor AHT10."""
#     init_command = [0xE1, 0x08, 0x00]  # Comando para inicializar o AHT10
#     i2c.transfer(I2C_ADDRESS, [I2C.Message(init_command)])  # Envia comando de inicialização
#     time.sleep(0.02)  # Aguarde 20ms para estabilização

# def aht10_read():
#     """Lê temperatura e umidade do sensor AHT10."""
#     # Envia comando para iniciar medição
#     measure_command = [0xAC, 0x33, 0x00]
#     i2c.transfer(I2C_ADDRESS, [I2C.Message(measure_command)])
#     time.sleep(0.08)  # Aguarde 80ms para conversão

#     # Lê os 6 bytes de dados do sensor
#     read_message = I2C.Message([0x00] * 6, read=True)
#     i2c.transfer(I2C_ADDRESS, [read_message])
#     data = read_message.data

#     # Processa os dados retornados
#     humidity_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
#     temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]

#     # Calcula umidade e temperatura reais
#     humidity = (humidity_raw / 1048576) * 100  # Em percentual
#     temperature = (temperature_raw / 1048576) * 200 - 50  # Em °C

#     return temperature, humidity

# # Main
# try:
#     aht10_init()  # Inicializa o sensor
#     temp, hum = aht10_read()  # Lê os valores de temperatura e umidade
#     print(f"Temperatura: {temp:.2f} °C, Umidade: {hum:.2f} %")
# finally:
#     i2c.close()  # Fecha o barramento I2C
