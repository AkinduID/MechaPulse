#include <ArduinoJson.h>
#include <WiFi.h>
#include <PubSubClient.h>
 
const char* ssid = "Galaxy M11126f";
const char* password =  "agcn7714";
const char* mqttServer = "192.168.45.190";
const int mqttPort = 1883;
const char* mqttUser = "neo";
const char* mqttPassword = "pixel";
 
WiFiClient espClient;
PubSubClient client(espClient);
 
void setup() {
 
  Serial.begin(115200);
  Serial.println();
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
 
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP32Client", mqttUser, mqttPassword )) {
 
      Serial.println("connected");
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
}
 
void loop() {
 
  StaticJsonBuffer<300> JSONbuffer;
  JsonObject& JSONencoder = JSONbuffer.createObject();
 
  JSONencoder["device"] = "ESP32";
  JSONencoder["sensorType"] = "Temperature";
  JsonArray& values = JSONencoder.createNestedArray("values");
 
  values.add(20);
  values.add(21);
  values.add(23);
 
  char JSONmessageBuffer[100];
  JSONencoder.printTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  Serial.println("Sending message to MQTT topic..");
  Serial.println(JSONmessageBuffer);
 
  if (client.publish("esp/test", JSONmessageBuffer) == true) {
    Serial.println("Success sending message");
  } else {
    Serial.println("Error sending message");
  }
 
  client.loop();
  Serial.println("-------------");
 
  delay(10000);
 
}
