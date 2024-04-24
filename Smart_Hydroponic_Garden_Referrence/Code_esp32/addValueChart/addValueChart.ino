#include <Arduino.h>

#include <EEPROM.h>
#include <SimpleTimer.h>
#include <Wire.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <String.h>


#define WIFI_SSID "Phong 18- 2.4G"
#define WIFI_PASSWORD "876543210"
#define FIREBASE_HOST "esp-firebase-f07dc-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "0b0IYc5BiY2q2SmleHQru4QvyyUmzdf9QRrF8zmD"
FirebaseData fbdb;

#define NTP_SERVER "pool.ntp.org"
#define NTP_TIMEZONE 7

float phValue, phVoltage;
float temp_water = 29, temp_air = 30, hum;
int count_chart=0;

String phValue_chart ="";
String hum_chart ="";
String temp_air_chart ="";
// WiFiUDP ntpUDP;
// NTPClient timeClient(ntpUDP, NTP_SERVER, NTP_TIMEZONE*3600,5000);

unsigned long previousMinute = 6;
// unsigned long currentMinute = 0;
// int count =0;
// int flag_time = 0;


void setup()
{
  Serial.begin(115200);
  // ec.begin();


  // timer_read_N_upload.setInterval(2000L,read_N_upload);
  // timer_upload_firebase.setInterval(5000L,upload_firebase);
  // timer_update_data.setInterval(1000L,update_data);

  // timeClient.begin();
  // timeClient.setTimeOffset(7 * 3600); // Đặt múi giờ (ở đây đang để cho múi giờ GMT+7)

  // previousMinute = timeClient.getMinutes();

  //Connect Wifi........................
  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
    Serial.print(".");
    delay(100);
  }

  Serial.println("\nConnected to the WiFi network");
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());

  //Connect Database.....................

  Firebase.begin(FIREBASE_HOST,FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  //set database read timeout to 1 minute (max 15min)
  Firebase.setReadTimeout(fbdb,1000*60);
  Firebase.setwriteSizeLimit(fbdb,"tiny");

  // timeClient.begin(); // Đặt múi giờ (ở đây đang để cho múi giờ GMT+7)

  // previousMinute = timeClient.getMinutes();
}
void loop()
{
  // timer_upload_firebase.run();
  // timer_read_N_upload.run();
  // timer_update_data.run();
  phValue = random(6,14);
  temp_air = random(28,30);
  hum = random(70,75);
  limit_value(24);

  // if (ph_chart.length() > 0) {
  //   ph_chart += ",";
      
  // }
  // ph_chart += String(phValue);
  // if (countOccurrences(ph_chart, ',') >= 24) {
  //   int firstCommaPos = ph_chart.indexOf(',');
  //   ph_chart = ph_chart.substring(firstCommaPos + 1);
  // }
  // // update_data();
  Serial.println(phValue_chart);
  // upload_firebase();
  delay(1000);
    
}
int countOccurrences(String str, char target) {
  int count = 0;
  for (size_t i = 0; i < str.length(); i++) {
    if (str.charAt(i) == target) {
      count++;
    }
  }
  return count;
}
void limit_value(int target){
  if(count_chart < target){
    hum_chart = add_value(hum_chart,String(hum));
    temp_air_chart = add_value(temp_air_chart,String(temp_air));
    phValue_chart = add_value(phValue_chart,String(previousMinute));
    phValue_chart+=":00";
    // add_value();
    count_chart++;
  } else{
    hum_chart = del_n_add_value(hum_chart,String(hum));
    temp_air_chart = del_n_add_value(temp_air_chart,String(temp_air));
    phValue_chart = del_n_add_value(phValue_chart,String(previousMinute));
    // del_n_add_value(String str);
  }
}

String del_n_add_value(String str, String value){
  int firstCommaPos = str.indexOf(',');
  str = str.substring(firstCommaPos + 1);
  str += ',';
  str += String(value);
  return str;
}
String add_value(String str, String value){
  if(str.length() > 0){
    str += ',';
    str += String(value);
  } else{
    str = String(value);
  }
  return str;
  
}
// void upload_firebase()
// {
//   Firebase.setString(fbdb,"/Chart/pH",ph_chart);

// }


