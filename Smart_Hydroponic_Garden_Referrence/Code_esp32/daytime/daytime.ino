#include <WiFi.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

const char* ssid = "Phong 18- 2.4G";
const char* password = "876543210";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org",7 * 3600,5000);

unsigned long previousMinute = 0;
unsigned long currentMinute = 0;
int count =0;
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  timeClient.begin();
  // timeClient.setTimeOffset(7 * 3600); // Đặt múi giờ (ở đây đang để cho múi giờ GMT+7)

  previousMinute = timeClient.getMinutes();
}

void loop() {
  if(timeClient.update()){
    currentMinute = timeClient.getMinutes();
    Serial.println(currentMinute);
  }
  
  if (currentMinute != previousMinute) {
    Serial.println(previousMinute);
    previousMinute = currentMinute;
    count+=1;
    Serial.println(currentMinute);
    Serial.println(count);
    Serial.println("Đã qua phút mới!");
    // Thực hiện các hành động cần thiết khi qua phút mới ở đây
  }
}
  
  // Tiếp tục thực hiện các công việc khác trong vòng lặp loop
  // ...

