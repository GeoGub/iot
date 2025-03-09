#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define DHTTYPE DHT11
#define DHTPIN D3
// #define SOUND_SENSOR_PIN A0

// WiFi настройки
const char* ssid = "TP-Link_7D87";
const char* password = "32666366";

// Серверная настройка
const char* server = "192.168.0.111";
const char* web_server = "http://192.168.0.111:1234";

// MQTT настройки
const int mqtt_port = 1883;
const char* tasks_topic = "tasks/controller/topic";
const char* result_topic = "result/controller/topic";

// Частота считывания показателей
const int DEFAULT_DELAY = 5 * 60 * 1000;

// Глобальные переменные
int lastTemperatureStatusCode;
int lastHumidityStatusCode;
int lastSoundStatusCode;

WiFiClient espClient;
HTTPClient http;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);

// Основные функции
void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(server, mqtt_port);
    client.setCallback(callback);
    dht.begin();
    reconnect();
}

void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();
  // int sound_level = analogRead(SOUND_SENSOR_PIN);

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  // Serial.print("Sound level: ");
  // Serial.println(sound_level);

  sendTemperature(temperature);
  sendHumidity(humidity);
  // sendSoundLevel(sound_level);

  customDelay();
}

// Подключение к WiFi
void setup_wifi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting..");
  }
  Serial.println(WiFi.localIP());
}

// MQTT функции
void callback(char* topic, byte* payload, unsigned int length) {
    Serial.print("Received message on topic: ");
    Serial.println(topic);
    Serial.print("Message: ");
    String task;
    String response_body;
    for (int i = 0; i < length; i++) {
        task += (char)payload[i];
        Serial.print((char)payload[i]);
    }
    Serial.println();
    if (task == "get_temperature") {
        float temperature = dht.readTemperature();
        if (isnan(temperature)) {
            response_body = "Failed to read temperature!";
        } else {
            response_body = "Current temperature - " + String(temperature) + "°C";
        }
    } else if (task == "get_humidity") {
      float humidity = dht.readHumidity();
      if (isnan(humidity)) {
        response_body = "Failed to read humidity!";
      } else {
        response_body = "Current humidity - " + String(humidity) + "%";
      }
    } else {
        response_body = "Unknown task!";
    }

    if (client.connected()) {
        client.publish(result_topic, response_body.c_str());
    } else {
        Serial.println("MQTT client not connected. Unable to publish response.");
    }

    Serial.println(response_body);
}

void reconnect() {
  Serial.print("Attempting MQTT connection...");
  if (client.connect("ESP32S3_Client")) {
      Serial.println("Connected!");
      client.subscribe(tasks_topic);
  } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
  }
}

// Функции отправки данных на web сервер
void sendTemperature(float temperature) {
    JsonDocument doc;
    char serializedDoc[256];

    doc["temperature"] = temperature;
    serializeJson(doc, serializedDoc);

    http.begin(espClient, String(web_server) + "/temperatures");
    http.addHeader("Content-Type", "application/json");

    lastTemperatureStatusCode = http.POST(serializedDoc);
    String payload = http.getString();

    Serial.println(lastTemperatureStatusCode);
    Serial.println(payload);

    http.end();
}

void sendHumidity(float humidity) {
    JsonDocument doc;
    char serializedDoc[256];

    doc["humidity"] = humidity;
    serializeJson(doc, serializedDoc);

    http.begin(espClient, String(web_server) + "/humidities");
    http.addHeader("Content-Type", "application/json");

    lastHumidityStatusCode = http.POST(serializedDoc);
    String payload = http.getString();

    Serial.println(lastHumidityStatusCode);
    Serial.println(payload);

    http.end();
}

void customDelay() {
  int delay_count = 0;

  while (delay_count < DEFAULT_DELAY) {
    if (!client.connected()) {
      reconnect();
      delay(5000);
      delay_count += 5000;
    } else {
      client.loop();
      delay(1000);
      delay_count += 1000;
    }
  }
}

// void sendSoundLevel(int sound_level) {
//     JsonDocument doc;
//     char serializedDoc[256];

//     doc["sound_level"] = sound_level;
//     serializeJson(doc, serializedDoc);

//     http.begin(espClient, "http://192.168.0.111:1234/sound-levels");
//     http.addHeader("Content-Type", "application/json");

//     lastSoundStatusCode = http.POST(serializedDoc);
//     String payload = http.getString();

//     Serial.println(lastSoundStatusCode);
//     Serial.println(payload);

//     http.end();
// }
