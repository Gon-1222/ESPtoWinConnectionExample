#include <WiFi.h>  // ESP32の場合 (ESP8266の場合は ESP8266WiFi.h)
#include <WiFiUdp.h>  // UDP用ライブラリ

const char* ssid = "Yourssid";      // WiFiのSSID
const char* password = "wifipassword";  // WiFiのパスワード
const char* udpAddress = "192.168.1.49";  // UDPサーバーのIPアドレス
const uint16_t udpPort = 1234;           // UDPサーバーのポート

WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  delay(100);

  // WiFiに接続
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // UDPサーバーに接続
  udp.begin(WiFi.localIP(), udpPort);
}

void loop() {
  // AnalogReadの値を読み取る
  int analogValue = analogRead(34); // A0ピンなど使用可能なアナログピンに変更

  // UDPパケット送信
  udp.beginPacket(udpAddress, udpPort);
  udp.print(String(analogValue));   // AnalogReadの値を送信
  udp.endPacket();

  Serial.print("Sent value: ");
  Serial.println(analogValue);       // デバッグ用に送信した値をシリアルに出力

  delay(100);  // 0.1秒ごとに送信
}
