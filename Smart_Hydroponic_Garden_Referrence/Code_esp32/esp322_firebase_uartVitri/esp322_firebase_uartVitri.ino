#include <WiFi.h>
#include <FirebaseESP32.h>

#define WIFI_SSID "Phong 18- 2.4G"
#define WIFI_PASSWORD "876543210"

#define FIREBASE_HOST "esp-firebase-f07dc-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "0b0IYc5BiY2q2SmleHQru4QvyyUmzdf9QRrF8zmD"

FirebaseData fbdb;


String pos_current= "";

void setup(){
  Serial.begin(115200);
  delay(1000);


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

}

void loop(){

  // updtae data to firebase...................
  Firebase.setInt(fbdb,"/Value/temp",random(0,100));
  Firebase.setInt(fbdb,"/Value/hum",random(0,100));
  Firebase.setInt(fbdb,"/Value/pH",random(0,100));
  Firebase.setInt(fbdb,"/Value/ppm",random(0,500));

  if(Firebase.getString(fbdb, "/Position/pos")==true){
    if(fbdb.stringData()!= pos_current){
      pos_current = fbdb.stringData();
      Serial.println(pos_current);
    }
  }
  // Serial.print(fbdb.stringData());
  // Control LED from firebase............
  // Firebase.getString(fbdb, "/Control/led");
  // if(Firebase.stringData() !=pos_current){
  //   pos_current = fbdb.to<String>();
  //   Serial.print(Firebase.getString(fbdb, "/Control/led");
  // }
  
}