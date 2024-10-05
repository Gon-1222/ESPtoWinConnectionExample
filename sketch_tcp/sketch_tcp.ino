#include <WiFi.h> // ESP32の場合 (ESP8266の場合は ESP8266WiFi.h)
 
const char* ssid = "yourssid";      // WiFiのSSID
const char* password = "wifipassword";  // WiFiのパスワード
const char* host = "192.168.1.49";  // TCPサーバーのIPアドレス
const uint16_t port = 1234;           // TCPサーバーのポート

WiFiClient client;

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

  // TCPサーバーに接続
  Serial.print("Connecting to ");
  Serial.println(host);

  if (!client.connect(host, port)) {
    Serial.println("Connection to server failed");
    return;
  }

  Serial.println("Connected to server");
}

void loop() {
  if (client.connected()) {
    int analogValue = analogRead(34); // A0ピンなど使用可能なアナログピンに変更
    client.print(String(analogValue)); // AnalogReadの値を送信
    client.print("\n");                // 改行を追加（サーバー側でパースしやすくするため）

    Serial.print("Sent value: ");
    Serial.println(analogValue);       // デバッグ用に送信した値をシリアルに出力

    delay(1000);  // 0.1秒ごとに送信
  } else {
    Serial.println("Disconnected from server");
    delay(1000); // 再接続のための待機時間
    client.connect(host, port); // サーバーへの再接続
  }
}
