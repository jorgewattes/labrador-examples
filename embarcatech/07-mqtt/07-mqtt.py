"""

sudo apt install mosquitto mosquitto-clients
mosquitto -v

mosquitto_pub -h test.mosquitto.org -t labrador/test -m "Teste"
mosquitto_sub -h test.mosquitto.org -t labrador/test


"""

import paho.mqtt.client as mqtt

# Configurações do broker MQTT
BROKER_ADDRESS = "test.mosquitto.org"  # Pode substituir pelo seu broker
BROKER_PORT = 1883  # Porta padrão para MQTT não seguro
TOPIC = "labrador/test"  # Tópico para subscrição/publicação

# Callback para conexão bem-sucedida ao broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado ao broker MQTT com sucesso!")
        client.subscribe(TOPIC)  # Subscrevendo ao tópico
    else:
        print(f"Erro de conexão: {rc}")

# Callback para mensagens recebidas
def on_message(client, userdata, msg):
    print(f"Mensagem recebida: {msg.payload.decode()} no tópico {msg.topic}")

# Callback para publicações bem-sucedidas
def on_publish(client, userdata, mid):
    print(f"Mensagem publicada com sucesso! ID: {mid}")

# Configurando o cliente MQTT
client = mqtt.Client("Labrador_Client")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Conexão ao broker
print("Conectando ao broker MQTT...")
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Publicando uma mensagem
message = "Olá do Labrador!"
client.publish(TOPIC, message)

# Mantendo o cliente MQTT ativo para escutar mensagens
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\nEncerrando o cliente MQTT.")
    client.disconnect()
