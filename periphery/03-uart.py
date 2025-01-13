"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/ttyS*

Pinos ttyS0
-UART0_TX: Header 17 - GPIOC27
-UART0_RX: Header 19 - GPIOC26

Realize o loopback conectando o Tx do Rx.
O valor enviado deverá ser o mesmo recebido.
"""

from periphery import Serial

# Open /dev/ttyUSB0 with baudrate 115200, and defaults of 8N1, no flow control
serial = Serial("/dev/ttyS0", 115200)



# Read up to 128 bytes with 500ms timeout
try:
    while(1):
        data_to_send = input("Dado a enviar: ").encode('utf-8')
        serial.write(data_to_send)
        data_readed = serial.read(len(data_to_send)).decode('utf-8')
        print(data_readed)
finally:
    serial.close()

# uart_device = "/dev/ttyS0"
# baudrate = 9600

# # # Inicializa a UART
# # try:
# #     uart = Serial(uart_device, baudrate)
# #     print(f"UART configurada no dispositivo {uart_device} a {baudrate} baud.")

# #     # Recebe os dados do usuário
# #     data_to_send = input("Digite os dados a serem enviados no loopback: ").encode('utf-8')

# #     # Envia os dados
# #     print(f"Enviando: {data_to_send}")
# #     uart.write(data_to_send)

# #     # Lê os dados recebidos
# #     print("Aguardando resposta no loopback...")
# #     received_data = uart.read(len(data_to_send))
    
# #     # Validação do loopback
# #     if received_data == data_to_send:
# #         print(f"Loopback bem-sucedido! Dados recebidos: {received_data.decode('utf-8')}")
# #     else:
# #         print(f"Erro no loopback.\nDados enviados: {data_to_send.decode('utf-8')}\nDados recebidos: {received_data.decode('utf-8')}")

# # except Exception as e:
# #     print(f"Erro ao configurar ou usar UART: {e}")
# # finally:
# #     # Fecha o dispositivo UART
# #     uart.close()
# #     print("UART fechada.")