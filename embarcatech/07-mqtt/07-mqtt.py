# from gpiozero import Button
import paho.mqtt.client as mqtt
import time

# Configurações do broker HiveMQ Cloud
BROKER = "dc48fcba406f4ae480f508359ef51e75.s1.eu.hivemq.cloud"  # Substitua pelo seu broker
PORT = 8883  # Porta segura (SSL/TLS)
USERNAME = "hivemq.webclient.1736993320918"  # Substitua pelo seu usuário
PASSWORD = "5J1a0>Mi$oW2:@PjTLqc"  # Substitua pela sua senha
TOPIC = "embarcatech"  # Tópico para envio

# Configuração do botão (GPIO)
# BUTTON_PIN = 17  # Substitua pelo pino GPIO ao qual o botão está conectado
# button = Button(BUTTON_PIN)

# Callback para conexão bem-sucedida
def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Conectado ao HiveMQ com sucesso!")
    else:
        print(f"Erro de conexão: {rc}")

# Função para enviar mensagem ao pressionar o botão
def send_character(character):
    # character = "A"  # Caractere que será enviado
    client.publish(TOPIC, character)
    print(f"Caractere '{character}' enviado!")

# Configurando o cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="Labrador_Client", protocol=mqtt.MQTTv311, transport="tcp")
client.username_pw_set(USERNAME, PASSWORD)  # Autenticação
client.tls_set()  # Conexão segura (SSL/TLS)

# Configurando callback
client.on_connect = on_connect

# Conectando ao broker
print("Conectando ao HiveMQ Cloud...")
client.connect(BROKER, PORT, 60)
time.sleep(1)
# Associando o evento do botão à função
# button.when_pressed = send_character

# Mantendo o cliente MQTT ativo
try:
    while True:
        client.loop_start()  # Loop em segundo plano para MQTT
        send_character(input('Escreva um texto para o MQTT: '))
# button.wait_for_press()  # Aguarda eventos do botão
except KeyboardInterrupt:
    print("\nEncerrando...")
    client.loop_stop()
    client.disconnect()













# """

# sudo apt install mosquitto mosquitto-clients
# mosquitto -v

# mosquitto_pub -h test.mosquitto.org -t labrador/test -m "Teste"
# mosquitto_sub -h test.mosquitto.org -t labrador/test


# """

# import paho.mqtt.client as mqtt

# # Configurações do broker MQTT
# BROKER_ADDRESS = "test.mosquitto.org"  # Pode substituir pelo seu broker
# BROKER_PORT = 1883  # Porta padrão para MQTT não seguro
# TOPIC = "labrador/test"  # Tópico para subscrição/publicação

# # Callback para conexão bem-sucedida ao broker
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Conectado ao broker MQTT com sucesso!")
#         client.subscribe(TOPIC)  # Subscrevendo ao tópico
#     else:
#         print(f"Erro de conexão: {rc}")

# # Callback para mensagens recebidas
# def on_message(client, userdata, msg):
#     print(f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}")

# # Callback para publicações bem-sucedidas
# def on_publish(client, userdata, mid):
#     print(f"Mensagem publicada com sucesso! ID: {mid}")

# # Configurando o cliente MQTT
# client = mqtt.Client("Labrador_Client")
# client.on_connect = on_connect
# client.on_message = on_message
# client.on_publish = on_publish

# # Conexão ao broker
# print("Conectando ao broker MQTT...")
# client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# # Publicando uma mensagem
# message = "Olá do Labrador!"
# client.publish(TOPIC, message)

# # Mantendo o cliente MQTT ativo para escutar mensagens
# try:
#     client.loop_forever()
# except KeyboardInterrupt:
#     print("\nEncerrando o cliente MQTT.")
#     client.disconnect()
