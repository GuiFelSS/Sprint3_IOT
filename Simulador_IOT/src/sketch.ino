#include <WiFi.h>
#include <PubSubClient.h>
#include "Ultrasonic.h"
#include <ArduinoJson.h>

// Substitua com as suas credenciais
const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.mqtt-dashboard.com";
const int mqtt_port = 1883;

// Configuração dos pinos
const int potPin = 34;
const int trigPin = 25;
const int echoPin = 26;
const int buzzerPin = 27;

// Variaveis da lógica
#define VAGA_ID "vaga_01"
const float DISTANCIA_MAX_OCUPACAO = 40; // cm, ajuste conforme a simulação
long ultimaPublicacao = 0;
const long INTERVALO_PUBLICACAO = 5000; // 5 segundos

// Objetos para os componentes
WiFiClient espClient;
PubSubClient client(espClient);
Ultrasonic ultrasonic(trigPin, echoPin);

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado!");
  Serial.println("Endereço IP: ");
  Serial.println(WiFi.localIP());
}

void reconnect_mqtt() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT...");
    // Tenta conectar com o ID do cliente da vaga
    if (client.connect(VAGA_ID)) {
      Serial.println(" conectado!");
      // Assina o tópico de comando
      client.subscribe("mottu/patio/" VAGA_ID "/comando");
    } else {
      Serial.print(" falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tenta de novo em 5 segundos");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensagem recebida no topico: [");
  Serial.print(topic);
  Serial.println("] ");

  // O buzzer ativa com qualquer mensagem recebida no tópico de comando
  // Lógica de alerta sonoro
  digitalWrite(buzzerPin, HIGH);
  delay(1000); // Toca por 1 segundo
  digitalWrite(buzzerPin, LOW);
  
  // Aqui você pode adicionar lógica mais complexa para diferentes comandos
}

void publicarStatus(String status, String motoId) {
  // Cria um documento JSON
  StaticJsonDocument<200> doc;
  doc["vaga_id"] = VAGA_ID;
  doc["status_ocupacao"] = status;
  doc["moto_id"] = motoId;
  doc["timestamp"] = millis();

  char payload[200];
  serializeJson(doc, payload);

  client.publish("mottu/patio/" VAGA_ID "/status", payload);
  Serial.print("Status publicado: ");
  Serial.println(payload);
}

void setup() {
  Serial.begin(115200);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);

  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect_mqtt();
  }
  client.loop();

  // Publicar status a cada 5 segundos
  if (millis() - ultimaPublicacao > INTERVALO_PUBLICACAO) {
    long distancia = ultrasonic.read();
    String motoId = "NENHUMA";
    String status = "livre";

    if (distancia < DISTANCIA_MAX_OCUPACAO) {
        status = "ocupada";
        // Simula a leitura do ID da moto com o potenciômetro
        int potValue = analogRead(potPin);
        int motoIdValue = map(potValue, 0, 4095, 1, 3); // Mapeia o valor para 1, 2 ou 3
        
        switch(motoIdValue) {
          case 1:
            motoId = "MOTTU-E";
            break;
          case 2:
            motoId = "MOTTU-POP";
            break;
          case 3:
            motoId = "MOTTU-SPORT";
            break;
        }
    }
    
    publicarStatus(status, motoId);
    ultimaPublicacao = millis();
  }
}