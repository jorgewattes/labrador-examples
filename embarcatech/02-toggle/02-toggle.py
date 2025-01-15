"""
 sudo chown caninos /dev/gpiochip*
 
 sudo chmod g+rw /dev/gpiochip*

 

1. Criar uma Regra Udev
As regras Udev permitem definir permissões automaticamente para dispositivos específicos.

Criar o arquivo de regras: No terminal, execute:

$ sudo nano /etc/udev/rules.d/99-gpio.rules

Adicionar as regras: Insira o seguinte conteúdo no arquivo:

SUBSYSTEM=="gpio", GROUP="caninos", MODE="0660"
KERNEL=="gpiochip*", GROUP="caninos", MODE="0660"

Salvar e sair: Pressione CTRL + O, Enter para salvar, e CTRL + X para sair.

Recarregar as regras Udev: Após criar o arquivo, atualize as regras do sistema:
$ sudo udevadm control --reload-rules
$ sudo udevadm trigger

2. Adicionar o Usuário ao Grupo
Certifique-se de que o usuário que você está utilizando pertence ao grupo caninos:

$ sudo usermod -aG caninos caninos

Reiniciar a sessão: Para aplicar as alterações, reinicie sua sessão no terminal ou o sistema.

3. Verificar as Alterações
Conecte o dispositivo e execute:

$ ls -l /dev/gpiochip*

Certifique-se de que os dispositivos estão associados ao grupo caninos com permissões rw-.
Com essas configurações, as permissões para o GPIO serão aplicadas automaticamente, e você não precisará inserir os comandos chown e chmod manualmente.


"""

#/dev/gpiochip0 - A
#/dev/gpiochip1 - B
#/dev/gpiochip2 - C
#/dev/gpiochip3 - D
#/dev/gpiochip4 - E

from periphery import GPIO
import time

# Configura o pino LED - GPIO /dev/gpiochip4; linha 2 (E2) como saída - GPIO-E2 (Header-5)
led = GPIO("/dev/gpiochip4", 2, "out") 

# Configura o pino Button - GPIO /dev/gpiochip4 line 3 (E3) como entrada - GPIO-E3 (Header-3)
button = GPIO("/dev/gpiochip4", 3, "in", bias="pull_up") 

try:
    while(1):  
        if(not button.read()): # Botão pressionado:
            led.write(not led.read()) 
            time.sleep(0.3) # Filtragem de bounce
finally:
    button.close()
    led.close()

