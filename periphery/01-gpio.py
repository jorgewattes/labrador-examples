"""1. Criar uma Regra Udev
As regras Udev permitem definir permissões automaticamente para dispositivos específicos.

Criar o arquivo de regras: No terminal, execute:

bash
Copiar código
sudo nano /etc/udev/rules.d/99-gpio.rules
Adicionar as regras: Insira o seguinte conteúdo no arquivo:

bash
Copiar código
SUBSYSTEM=="gpio", GROUP="caninos", MODE="0660"
KERNEL=="gpiochip*", GROUP="caninos", MODE="0660"
Salvar e sair: Pressione CTRL + O, Enter para salvar, e CTRL + X para sair.

Recarregar as regras Udev: Após criar o arquivo, atualize as regras do sistema:

bash
Copiar código
sudo udevadm control --reload-rules
sudo udevadm trigger
2. Adicionar o Usuário ao Grupo
Certifique-se de que o usuário que você está utilizando pertence ao grupo caninos:

Adicionar o usuário ao grupo: Substitua seu_usuario pelo nome do usuário que você utiliza:

bash
Copiar código
sudo usermod -aG caninos seu_usuario
Reiniciar a sessão: Para aplicar as alterações, reinicie sua sessão no terminal ou o sistema.

3. Verificar as Alterações
Após configurar as permissões:

Conecte o dispositivo e execute:
bash
Copiar código
ls -l /dev/gpiochip*
Certifique-se de que os dispositivos estão associados ao grupo caninos com permissões rw-.
Com essas configurações, as permissões para o GPIO serão aplicadas automaticamente, e você não precisará inserir os comandos chown e chmod manualmente.

 sudo chown caninos /dev/gpiochip*
 
 sudo chmod g+rw /dev/gpiochip*

"""


from periphery import GPIO
import time

#GPIO-D17 - LED (BLUE)
#/dev/gpiochip0 - A
#/dev/gpiochip1 - B
#/dev/gpiochip2 - C
#/dev/gpiochip3 - D
#/dev/gpiochip4 - E

# Open LED - GPIO /dev/gpiochip0 line 17 with input direction
led = GPIO("/dev/gpiochip3", 17, "out") # GPIO-D17

# Open Button - GPIO /dev/gpiochip0 line 3 with output direction
button = GPIO("/dev/gpiochip4", 3, "in", bias="pull_up") # GPIO-E3 (Header-3)

try:
    while(1):    
        if(not button.read()): # If button pressed:
            led.write(not led.read()) 
            time.sleep(0.3) # Delay to bounce filter
finally:
    button.close()
    led.close()

