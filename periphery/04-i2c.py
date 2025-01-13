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


from periphery import Serial

def main():
    # Configure o dispositivo UART (substitua '/dev/ttyS0' pelo dispositivo correto no Labrador)
    uart_device = "/dev/ttyS0"
    baudrate = 9600

    # Inicializa a UART
    try:
        uart = Serial(uart_device, baudrate)
        print(f"UART configurada no dispositivo {uart_device} a {baudrate} baud.")

        # Recebe os dados do usuário
        data_to_send = input("Digite os dados a serem enviados no loopback: ").encode('utf-8')

        # Envia os dados
        print(f"Enviando: {data_to_send}")
        uart.write(data_to_send)

        # Lê os dados recebidos
        print("Aguardando resposta no loopback...")
        received_data = uart.read(len(data_to_send))
        
        # Validação do loopback
        if received_data == data_to_send:
            print(f"Loopback bem-sucedido! Dados recebidos: {received_data.decode('utf-8')}")
        else:
            print(f"Erro no loopback.\nDados enviados: {data_to_send.decode('utf-8')}\nDados recebidos: {received_data.decode('utf-8')}")

    except Exception as e:
        print(f"Erro ao configurar ou usar UART: {e}")
    finally:
        # Fecha o dispositivo UART
        uart.close()
        print("UART fechada.")

if __name__ == "__main__":
    main()





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
