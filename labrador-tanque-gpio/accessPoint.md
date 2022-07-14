# Configurando um Access Point

Uma boa maneira de se conectar ao Tanque é via rede Wifi, entretanto, não é muito prático depender de conexões Wifi externas pelos seguintes problemas:

1. Seria necessário conectar a Labrador a um monitor e a mouse/teclado para poder conectar-la à rede.
2. O Tanque ficaria dependente da existência de uma rede Wifi para poder funcionar
3. Seria necessário saber o endereço IP da Labrador para que a conexão fosse efetuada e os comandos fossem enviados.

Uma solução seria configurar a Labrador para que ela funcione como access point, dessa forma o endereço IP seria fixado, a própria placa iria prover a conexão evitando dependência de redes externas e, por meio de uma inicialização automatizada do access point, não seria necessário ligá-la a um monitor para concluir a conexão.

Os passos para configurar um access point simples serão mostrados nos tópicos a seguir.

## Access Point com Hostapd e DNSMasq

### Hostapd

Uma forma de transformar a Labrador em access point é o uso do hostapd.
O passo mais importante a ser feito para utilizar o hostapd é a sua correta configuração. O processo de configuração do hostapd consiste em alterar um arquivo com os parâmetros desejados. Antes de começar a usar o hostapd é necessário instalá-lo a partir do seguinte comando:

    sudo apt-get install hostapd

Para criar um arquivo de configuração utilize um editor de texto de sua preferência, usando o mousepad da labrador temos:

    sudo mousepad /etc/hostapd/hostapd.conf

Executando esse comando será aberto o editor de texto gráfico da Labrador. 

O arquivo de configuração precisa de algumas informações sobre o access point a ser criado como:
- Nome da interface Wifi
  - Pode ser obtida a partir do comando `sudo iw dev`, caso o comando não seja encontrado pode ser necessário instalar o pacote por meio do comando `sudo apt-get install iw`
- SSID
  - O nome da rede que aparecerá para os dispositivos que desejarem estabelecer uma comunicação
- Senha de acesso
  - Marcada pelo nome 'wpa_passphrase' no arquivo de edição

``` bash
# nome da interface Wifi
interface=wlan0
driver=nl80211
# Nome da rede
ssid=roverWifi
hw_mode=g
channel=6
macaddr_acl=0
ignore_broadcast_ssid=0
auth_algs=1
wpa=3
# senha da rede
wpa_passphrase=myPassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

Ao preencher o arquivo com as informações acima basta salvar o arquivo.

---

#### Testando o arquivo de configuração

Para testar o arquivo de configuração bastar executar o seguinte comando:

    sudo hostapd /etc/hostapd/hostapd.conf

Caso o comando não seja reconhecido, verifique se o hostapd foi corretamente instalado ou tente executar pelo seguinte comando:

    sudo /usr/sbin/hostapd /etc/hostapd/hostapd.conf

Ao executar com êxito a Labrador começará a funcionar como access point e a rede poderá ser identificada por outros dispositivos. Nesse ponto ainda não será possível conectar corretamente à Labrador devido à falta de um servidor DHCP (uma alternativa seria configurar um IP fixo no dispositivo, entretanto, essa não é uma situação desejada devido ao trabalho adicional exigido).

---

### DNSMasq

Como dito anteriormente não é possível conectar corretamente à rede recém criada devido à ausência de um servidor DHCP. Para essa função será utilizado o DNSMasq.

Para instalar o DNSMasq basta executar o seguinte comando:

    sudo apt-get install dnsmasq

Para configurar o DNSMasq iremos alterar outro arquivo config:

    sudo mousepad /etc/dnsmasq.conf

Um exemplo de coniguração possível é mostrada a seguir:

``` bash
# Interface
interface=wlan0
# Range de ips a serem atribuidos pros clientes e o tempo de concessão
dhcp-range=10.0.0.3,10.0.0.20,12h
```

---
#### Testando o Access Point

Terminados os passos mostrados é necessário iniciar o DNSMasq e o Hostapd adequadamente:

``` bash
$ ip link set wlan0 down
$ ip addr flush dev wlan0
$ ip link set wlan0 up
$ ip addr add 10.0.0.1/24 dev wlan0
$ sudo killall dnsmasq
$ sudo dnsmasq
$ sudo hostapd /etc/hostapd/hostapd.conf
```

Após a execução dessa sequência de comandos o access point deve estar funcionando e aceitando conexões com outros dispositivos e o endereço IP na rede recém criada será $10.0.0.1$

---

## Auto-start do access point

Seria interessante que o access point iniciasse sozinho para evitar a necessidade de abrir o terminal e digitar a sequência de comandos para habilitar o access point.

O primeiro passo para iniciar o access point automaticamente é criar um bash script com os respectivos comandos. Para isso, abra o editor de sua preferência e inclua os comandos de inicialização:

``` sh
sudo ip link set wlan0 down
sudo ip addr flush dev wlan0
sudo ip link set wlan0 up
sudo ip addr add 10.0.0.1/24 dev wlan0

sleep 2

if [ -z "$(ps -e | grep dnsmasq)" ]
then
 dnsmasq
fi

# A opção -B faz com que o hostapd execute em background
sudo /usr/sbin/hostapd -B /etc/hostapd/hostapd-teste.conf
```

Basta então salvar o arquivo com a extensão .sh e torná-lo executável com o comando:

    sudo chmode +x <caminho para o arquivo .sh> 

Feito isso o script está pronto para ser chamado durante a inicialização do sistema.

---

### Executando após a inicialização da GUI

Uma opção é executar o script após a Inicialização da Interface com o usuário. Para isso basta editar o arquivo de autostart:

    sudo mousepad /etc/xdg/lxsession/LXDE/autostart

Adicionando a seguinte linha:

    @sh /home/caninos/--caminho para o arquivo .sh--/nome_do_script.sh

Feito isso o script criado será executado qdo a interface for aberta e o access point começará a funcionar. 

#### Desabilitando a tela de login

:qInfelizmente a alternativa apresentada só funciona após o login. Entretanto, é possível desabilitar o login, alterando o arquivo `/etc/lightdm/lightdm.conf`:

    sudo mousepad /etc/lightdm/lightdm.conf

No arquivo garanta que os seguintes campos sejam alterados/incluídos para conter os seguintes valores:

```
[Seat:*]
pam-service=lightdm
pam-autologin-service=lightdm-autologin
autologin-user=TYPE-YOUR-USERNAME-HERE
autologin-user-timeout=0
session-wrapper=/etc/X11/Xsession
greeter-session=lightdm-greeter
```

Basta então Salvar as alterações e, ao reiniciar a Labrador, não será necessário fazer login e o access point será iniciado automaticamente.

### Executando antes do Login

Outra opção de inicialização do access point é iniciá-lo durante o boot. Para isso crie o arquivo `/etc/rc.local`:

    sudo mousepad /etc/rc.local

Por padrão o arquivo contém o seguinte conteúdo:

``` bash
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

exit 0
```

O mais importante é que o arquivo termine com `exit 0` mas, se preferir, copie e cole todo o conteúdo (incluindo comentários). Inclua o script de inicialização do access point com seu caminho completo antes do `exit 0`:

``` bash
...
/home/caninos/--caminho--/nome_do_script.sh
exit 0
```

Salve o arquivo e torne-o executável: 

    sudo chmode +x /etc/rc.local

Após a reinicialização o access point será automaticamente configurado durante o boot da labrador

# Controlando a Labrador via SSH

Com o access point configurado podemos nos conectar facilmente à Labrador, mas como aproveitar isso para controlá-la remotamente?
Existem inúmeras formas de responder a essa pergunta mas, nesse tópico, será abordada a conexão via SSH.

Para conectar-se via SSH com a caninos basta conectar o dispositivo que irá enviar os comandos à rede Wifi recém criada. Se a rede foi configurada seguindo os mesmos passos apresentados aqui o endereço IP da Labrador será `10.0.0.1` e  para conectar via ssh utilizamos o comando:

    ssh caninos@10.0.0.1

- Note que o comando ssh é composto pelo nome do usuário unido ao endereço IP da placa por um '@', sendo assim o comando deve ser alterado para refletir o usuário  que está solicitando login.
- Esse comando pode ser executado via terminal de comandos no Linux, no Mac e nas versões mais recentes do Windows. No caso de versões mais antigas do Windows é necessário instalar algum cliente SSH.

Ao solicitar o acesso será solicitada a senha do usuário fornecido. Após a inserção da senha o terminal de comandos passará a controlar remotamente a Labrador sendo possível, por exemplo, a execução de códigos previamente criados.

## Instalando o servidor SSH na Labrador

Caso a conexão à Labrador via SSH não funcione é possível que o servidor SSH não esteja instalado. O processo de instalação é bem simples como o de qualquer outro pacote:

    sudo apt-get install openssh-server
    

