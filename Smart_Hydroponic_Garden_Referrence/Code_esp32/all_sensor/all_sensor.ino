#include <Arduino.h>
#include <OneWire.h>
#include <Wire.h>
#include "DFRobot_ESP_PH.h"  
// #include <DFRobot_ESP_EC.h>
#include "GravityTDS.h"
#include <DallasTemperature.h>
#include <EEPROM.h>
#include <SimpleTimer.h>
#include <Wire.h>
#include <BH1750.h>
#include <SHT3x.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#define TdsSensorPin A0
GravityTDS gravityTds;

#define WIFI_SSID "Phong 18- 2.4G"
#define WIFI_PASSWORD "876543210"
#define FIREBASE_HOST "esp-firebase-f07dc-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "0b0IYc5BiY2q2SmleHQru4QvyyUmzdf9QRrF8zmD"
FirebaseData fbdb;

#define NTP_SERVER "pool.ntp.org"
#define NTP_TIMEZONE 7

#define ONE_WIRE_BUS 4                // this is the gpio pin 13 on esp32.
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

#define ESPADC 4096.0   //the esp Analog Digital Convertion value
#define ESPVOLTAGE 3300

SHT3x Sensor;
BH1750 lightMeter;
SimpleTimer timer_read_N_upload;
// SimpleTimer timer_upload_firebase;
SimpleTimer timer_update_data;
// DFRobot_ESP_EC ec;
DFRobot_ESP_PH ph;

float phValue, phVoltage;
float temp_water = 29, temp_air = 30, hum;
int lux,ppmValue;
String target_pH ;
String target_EC ;
String target_GrowLight,target_GrowLight_auto,Grow_Light_SetTime,start_hour, start_min;
String data_trans;
String auto_mode,grown_up;

String phValue_chart ="4.68,4.62,4.68,4.64,4.58,4.68,4.66,4.67,4.62,4.63,4.67,4.64,4.55,4.63,4.62,4.58,4.57,4.51,4.57,4.58,4.65,4.60,4.64,4.64";
String hum_chart ="78.17,74.92,75.99,76.15,78.45,78.57,79.98,80.80,81.88,81.45,80.90,79.68,76.81,70.90,69.22,68.59,69.05,68.87,71.40,70.16,72.36,72.46,72.88,73.81";
String temp_air_chart ="30.43,29.78,29.51,29.47,29.03,28.92,28.69,28.52,28.55,28.92,29.18,29.51,30.01,30.98,31.11,31.38,31.38,31.34,31.31,31.16,30.98,30.89,30.80,30.55";
String ppmValue_chart ="1470,1487,1482,1480,1489,1492,1500,1500,1489,1487,1474,1482,1476,1459,1458,1456,1455,1452,1449,1448,1460,1453,1460,1461";
String time_chart ="0:00,1:00,2:00,3:00,4:00,5:00,6:00,7:00,8:00,9:00,10:00,11:00,13:00,14:00,15:00,16:00,17:00,18:00,19:00,20:00,21:00,22:00,23:00,0:00";

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, NTP_SERVER, NTP_TIMEZONE*3600,5000);

unsigned long previousMinute = 0;
unsigned long currentMinute = 0;
unsigned long previousHours = 25;
unsigned long currentHours = 0;
int count =0;
int flag_time = 0;
int count_chart=0;
int flag_chart = 0;


float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
  sensors.requestTemperatures();
  return sensors.getTempCByIndex(0);
  
}



void setup()
{
  Serial.begin(115200);
  EEPROM.begin(32);//needed EEPROM.begin to store calibration k in eeprom
  ph.begin();
  // ec.begin();
  sensors.begin();
  Wire.begin();
  lightMeter.begin();
  Sensor.Begin();
  gravityTds.setPin(TdsSensorPin);
  gravityTds.setAref(3.3);  //reference voltage on ADC, default 5.0V on Arduino UNO
  gravityTds.setAdcRange(4096);  //1024 for 10bit ADC;4096 for 12bit ADC
  gravityTds.setKvalue(1.20);
  gravityTds.begin();

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

  timeClient.begin(); // Đặt múi giờ (ở đây đang để cho múi giờ GMT+7)

  // previousMinute = timeClient.getMinutes();
        // currentMinute = timeClient.getMinutes();
  // previousHours = timeClient.getHours();
}

void loop()
{
    // timer_upload_firebase.run();
    // timer_read_N_upload.run();
    read_N_upload();
    // timer_update_data.run();
    update_data();
    
}

void read_N_upload()
{
  unsigned long last = millis();
  // for(int i = 0; i<5;i++){
    temp_water = readTemperature();  // read your temperature sensor to execute temperature compensation
    temp_water = roundToDecimal(temp_water,2);

    gravityTds.setTemperature(temp_water);  // set the temperature and execute temperature compensation
    gravityTds.update();  //sample and calculate 
    ppmValue = gravityTds.getTdsValue();

    phVoltage = analogRead(A3) / ESPADC * ESPVOLTAGE;
    phValue = ph.readPH(phVoltage, temp_water); // convert voltage to pH with temperature compensation
    phValue = roundToDecimal(phValue,2); // convert voltage to pH with temperature compensation
    
    lux = lightMeter.readLightLevel()*5;

    Sensor.UpdateData();
    temp_air = Sensor.GetTemperature();
    temp_air = roundToDecimal(temp_air,2);
    hum = Sensor.GetRelHumidity();
    hum = roundToDecimal(hum,2);
    Serial.println(millis()-last);
    upload_firebase();
    Serial.println(millis()-last);
}

void upload_firebase()
{
  Firebase.setInt(fbdb,"/Value/temp_water",temp_water);
  Firebase.setInt(fbdb,"/Value/temp_air",temp_air);
  Firebase.setInt(fbdb,"/Value/hum",hum);
  Firebase.setInt(fbdb,"/Value/lux",lux);
  Firebase.setInt(fbdb,"/Value/pH",phValue);
  Firebase.setInt(fbdb,"/Value/ppm",ppmValue);
}
void update_data(){
  checkAndUpdateData("/Check_mode",auto_mode);
  if(auto_mode=="0"){
    checkAndUpdateData("/Control/led", target_GrowLight);
    checkAndUpdateData("/Control/ph", target_pH);
    checkAndUpdateData("/Control/ppm", target_EC);
    data_trans=String(phValue) + "/" + 
                    String(ppmValue) + "/" + 
                    target_pH + "/" + 
                    target_EC + "/" + 
                    target_GrowLight;
    Serial.println(data_trans);
  } else {
    checkAndUpdateData("/grown_up",grown_up);
    checkAndUpdateData("/Timer_lighting/hour", start_hour);
    checkAndUpdateData("/Timer_lighting/min", start_min);
    if(grown_up == "0"){
      checkAndUpdateData("/Auto_1/led", target_GrowLight);
      checkAndUpdateData("/Auto_1/ph", target_pH);
      checkAndUpdateData("/Auto_1/ppm", target_EC);
      checkAndUpdateData("/Auto_1/time",Grow_Light_SetTime);
      // checkAndUpdateData("/Auto_1/start_hour",start_hour);
    } else {
      checkAndUpdateData("/Auto_2/led", target_GrowLight);
      checkAndUpdateData("/Auto_2/ph", target_pH);
      checkAndUpdateData("/Auto_2/ppm", target_EC);
      checkAndUpdateData("/Auto_2/time",Grow_Light_SetTime);
      // checkAndUpdateData("/Auto_2/start_hour",start_hour);
    }
      if(timeClient.update()){
        currentMinute = timeClient.getMinutes();
        currentHours = timeClient.getHours();
      }
      if(flag_time){
        
        if (currentMinute != previousMinute) {
          Serial.println(previousMinute);
          previousMinute = currentMinute;
          count+=1;
          Serial.println(count);
          Serial.println((int)(Grow_Light_SetTime.toFloat()*60));
        }
        if(count < (int)(Grow_Light_SetTime.toFloat()*60)){
          target_GrowLight_auto = target_GrowLight;
        } else {
          target_GrowLight_auto = "0";
          flag_time = 0;
          count = 0;
        }
      } else {
          if(currentHours==start_hour.toInt() && currentMinute==start_min.toInt()){
          flag_time=1;
          previousMinute = currentMinute;
          Serial.println("flag");
          }
      }
      if(currentMinute == 0 && flag_chart == 0){
        Chart_value(24);
        flag_chart = 1;
      } 
      if(currentMinute == 1){
        flag_chart = 0;
      }
      

      // if(currentMinute != previousMinute){
      //   Chart_value(24);
      //   previousMinute = currentMinute;
      // }

    data_trans=String(phValue) + "/" + 
                    String(ppmValue) + "/" + 
                    target_pH + "/" + 
                    
                    target_EC + "/" + 
                    target_GrowLight_auto;
    Serial.println(data_trans);
  }
  
}
void checkAndUpdateData(const String& controlPath, String& target) {
  if (Firebase.getString(fbdb, controlPath)) {
    String controlValue = fbdb.stringData();

    if (controlValue != target) {
      target = controlValue;
      // Serial.println(target);
    }
  }

}

float roundToDecimal(float number, int decimalPlaces) {
  float multiplier = pow(10, decimalPlaces);
  return round(number * multiplier) / multiplier;
}

// float filter_data(float data){
// 	return roundToDecimal(filter.updateEstimate(data),2);
// }
void Chart_value(int target){
  if(count_chart < target){
    hum_chart = add_value(hum_chart,String(hum));
    temp_air_chart = add_value(temp_air_chart,String(temp_air));
    phValue_chart = add_value(phValue_chart,String(phValue));
    ppmValue_chart = add_value(ppmValue_chart,String(ppmValue));
    time_chart = add_value(time_chart,String(currentHours));
    time_chart += ":00";
    // add_value();
    count_chart++;
  } else{
    hum_chart = del_n_add_value(hum_chart,String(hum));
    temp_air_chart = del_n_add_value(temp_air_chart,String(temp_air));
    phValue_chart = del_n_add_value(phValue_chart,String(phValue));
    ppmValue_chart = del_n_add_value(ppmValue_chart,String(ppmValue));
    time_chart = del_n_add_value(time_chart,String(currentHours));
    time_chart += ":00";
    // del_n_add_value(String str);
  }
  Firebase.setString(fbdb,"/Chart/Hum",hum_chart);
  Firebase.setString(fbdb,"/Chart/Temp",temp_air_chart);
  Firebase.setString(fbdb,"/Chart/pH",phValue_chart);
  Firebase.setString(fbdb,"/Chart/ppm",ppmValue_chart);
  Firebase.setString(fbdb,"/Chart/Time",time_chart);
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
