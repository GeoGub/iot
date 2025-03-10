#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define DHTTYPE DHT11
#define DHTPIN D3

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

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

int16_t x, y;
uint16_t textWidth, textHeight;

WiFiClient espClient;
HTTPClient http;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Основные функции
void setup() {
  Serial.begin(115200);
  setupWiFi();
  client.setServer(server, mqtt_port);
  client.setCallback(callback);
  dht.begin();
  mqttConnect();

  Serial.println("Try to show message on display");

  if(display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    display.display(); // Выводим стартовое изображение

    delay(2000); // Пауза 2 секунды

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);

    // String text = "Temperature: 10°C";
    String text = "Await to get current readings";
    display.getTextBounds(text, 0, 0, &x, &y, &textWidth, &textHeight);

    // Позиционируем текст по центру
    int posX = (SCREEN_WIDTH - textWidth) / 2;
    int posY = (SCREEN_HEIGHT - textHeight) / 2;

    display.setCursor(posX, posY);
    display.println(text);
    display.display();  // Обновляем экран
  }
}

void loop() {

  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  displayCurrentValues(temperature, humidity);

  Serial.print("Temperature: ");
  Serial.println(temperature);

  Serial.print("Humidity: ");
  Serial.println(humidity);

  sendTemperature(temperature);
  sendHumidity(humidity);

  customDelay();
}

void displayCurrentValues(float temperature, float humidity) {
  String line1 = "Temperature: " + String(temperature) + "°C";
  String line2 = "Humidity:" + String(humidity) + "%";

  Serial.println(line1);
  Serial.println(line2);

  Serial.println("Clear display");

  display.clearDisplay();

  // 1 строка
  display.getTextBounds(line1, 0, 0, &x, &y, &textWidth, &textHeight);
  int posX1 = 0;
  int posY1 = (SCREEN_HEIGHT - 2 * textHeight) / 3;
  display.setCursor(posX1, posY1);
  display.println(line1);

  // 2 строка
  display.getTextBounds(line2, 0, 0, &x, &y, &textWidth, &textHeight);
  int posX2 = 0;
  int posY2 = posY1 + textHeight + 4;
  display.setCursor(posX2, posY2);
  display.println(line2);

  Serial.println("Display lines");
  // Обновляем изображение
  display.display();
}

// Подключение к WiFi
void setupWiFi() {
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

void mqttConnect() {
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
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    displayCurrentValues(temperature, humidity);

    if (!client.connected()) {
      mqttConnect();
    } else {
      client.loop();
    }
    delay(1000);
    delay_count += 1000;
  }
}
