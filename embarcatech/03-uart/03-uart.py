"""
Liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/ttyS*

Pinos ttyS0
-UART0_TX: Header 08 - GPIOC27
-UART0_RX: Header 10 - GPIOC26

Realize o loopback conectando o Tx do Rx.
O valor enviado deverá ser o mesmo recebido.
"""

from periphery import Serial

# Configura a serial /dev/ttyUSB0 com baudrate 9600
serial = Serial("/dev/ttyS0", 9600)

while(1):
    data_to_send = input("Dado a enviar: ").encode('utf-8')
    serial.write(data_to_send)
    data_readed = serial.read(len(data_to_send)).decode('utf-8')
    print(f'Dado recebido:{data_readed}')
