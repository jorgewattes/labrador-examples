"""
3. Exemplo de configuração no Linux
Suponha que você quer usar os pinos GPIO 14 (TX) e GPIO 15 (RX). No sistema operacional:

Verificar se os pinos estão configurados para UART:
$ gpio readall

Configurar os pinos:
Se necessário, ajuste os pinos para a função UART, como:


$ config-pin P9.24 uart  # Exemplo para TX
$ config-pin P9.26 uart  # Exemplo para RX

Verificar se o UART está ativo:
Depois de configurar os pinos, liste os dispositivos UART no sistema para garantir que estão habilitados:

$ ls /dev/ttyS*


void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
}

void loop() {
  if (Serial.available()) {        // If anything comes in Serial (USB),
    Serial1.write(Serial.read());  // read it and send it out Serial1 (pins 0 & 1)
  }

  if (Serial1.available()) {       // If anything comes in Serial1 (pins 0 & 1)
    Serial.write(Serial1.read());  // read it and send it out Serial (USB)
  }
}
"""

from periphery import Serial

# Open /dev/ttyUSB0 with baudrate 115200, and defaults of 8N1, no flow control
serial = Serial("/dev/ttyS0", 115200)

serial.write(b"Hello World!")

# Read up to 128 bytes with 500ms timeout
try:
    while(1):
        buf = serial.read(128, 0.5)
        print(buf)
finally:
    serial.close()