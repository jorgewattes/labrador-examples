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
        data_to_send = input("Dado a enviar: ")
        serial.write(data_to_send)
        data_readed = serial.read(128, 0.5)
        print(data_readed)
finally:
    serial.close()