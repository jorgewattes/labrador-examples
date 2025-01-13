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

# Configuração do barramento I2C
i2c = I2C("/dev/i2c-2")

# Fonte simples de 5x8 pixels para caracteres ASCII (0x20 a 0x7F)
FONT_5x8 = {
    " ": [0x00, 0x00, 0x00, 0x00, 0x00],
    "H": [0x7C, 0x12, 0x12, 0x7C, 0x00],
    "e": [0x3C, 0x4A, 0x4A, 0x30, 0x00],
    "l": [0x00, 0x00, 0x7E, 0x00, 0x00],
    "o": [0x3C, 0x42, 0x42, 0x3C, 0x00],
    "W": [0x7C, 0x02, 0x02, 0x7C, 0x00],
    "r": [0x00, 0x7C, 0x12, 0x12, 0x00],
    "d": [0x3C, 0x42, 0x42, 0x3C, 0x00],
    "!": [0x00, 0x00, 0x5E, 0x00, 0x00]
}

def ssd1306_init():
    """Inicializa o display SSD1306."""
    commands = [
        0xAE,  # Display OFF
        0xD5, 0x80,  # Set Display Clock Divide Ratio/Oscillator Frequency
        0xA8, 0x3F,  # Set Multiplex Ratio (1/64)
        0xD3, 0x00,  # Set Display Offset
        0x40,  # Set Display Start Line
        0x8D, 0x14,  # Charge Pump Setting (Enable)
        0x20, 0x00,  # Set Memory Addressing Mode (Horizontal Addressing)
        0xA1,  # Set Segment Re-map
        0xC8,  # Set COM Output Scan Direction
        0xDA, 0x12,  # Set COM Pins Hardware Configuration
        0x81, 0xCF,  # Set Contrast Control
        0xD9, 0xF1,  # Set Pre-charge Period
        0xDB, 0x40,  # Set VCOMH Deselect Level
        0xA4,  # Entire Display ON
        0xA6,  # Normal Display (A6=Normal, A7=Inverse)
        0xAF   # Display ON
    ]
    for cmd in commands:
        i2c.transfer(I2C_ADDRESS, [I2C.Message([0x00, cmd])])

def ssd1306_clear():
    """Limpa o display."""
    buffer = [0x40] + [0x00] * 1024
    i2c.transfer(I2C_ADDRESS, [I2C.Message(buffer)])

def ssd1306_write_text(text, x=0, y=0):
    """
    Escreve texto em uma posição específica.
    - text: texto a ser exibido
    - x: posição horizontal (0 a 127)
    - y: posição vertical (0 a 7, cada unidade é uma página de 8 pixels)
    """
    # Define a posição inicial
    commands = [
        0xB0 + y,  # Define a página (linha vertical)
        0x00 + (x & 0x0F),  # Define coluna baixa
        0x10 + ((x >> 4) & 0x0F)  # Define coluna alta
    ]
    for cmd in commands:
        i2c.transfer(I2C_ADDRESS, [I2C.Message([0x00, cmd])])

    # Constrói o buffer do texto
    buffer = [0x40]  # Prefixo de dados
    for char in text:
        buffer.extend(FONT_5x8.get(char, [0x00] * 5))  # Cada caractere ocupa 5 colunas
        buffer.append(0x00)  # Espaço entre caracteres

    # Envia os dados
    for i in range(0, len(buffer), 16):  # Divide em blocos de 16 bytes
        i2c.transfer(I2C_ADDRESS, [I2C.Message(buffer[i:i+16])])

# Execução
try:
    ssd1306_init()  # Inicializa o display
    ssd1306_clear()  # Limpa o display
    ssd1306_write_text("Hello, World!", x=0, y=0)  # Escreve na posição inicial
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
