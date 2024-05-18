#include <SimpleTimer.h>

//TDS Sensor and ESP32
// Download Libraries

#include <Arduino.h>
#include <OneWire.h>
#include <Wire.h>
// #include <DFRobot_ESP_PH_WITH_ADC.h> 
#include "DFRobot_ESP_PH.h"
// #include <Adafruit_ADS1015.h>     
#include <DFRobot_ESP_EC.h>
#include <DallasTemperature.h>
#include <EEPROM.h>
// #include <BlynkSimpleEsp32.h>
#include <SimpleTimer.h>

#define ONE_WIRE_BUS 4                // this is the gpio pin 13 on esp32.
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

DFRobot_ESP_EC ec;
DFRobot_ESP_PH ph;
#define ESPADC 4096.0   //the esp Analog Digital Convertion value
#define ESPVOLTAGE 3300
// Adafruit_ADS1115 ads;

float phvoltage, phValue;
float TDSvoltage, ecValue, temperature = 25;

// You should get Auth Token in the Blynk App.
// char auth[] = "I_r9XZkkR4bKYnfPptszNQy2zvcjPm4O";

// // Your WiFi credentials.
// // Set password to "" for open networks.
// char ssid[] = "AndroidAP7DF8";
// char pass[] = "electroniclinic";
SimpleTimer timer;


float readTemperature()
{
  //add your code here to get the temperature from your temperature sensor
  sensors.requestTemperatures();
  return sensors.getTempCByIndex(0);
  
}

void setup()
{
  Serial.begin(115200);
    // Blynk.begin(auth, ssid, pass);
  EEPROM.begin(32);//needed EEPROM.begin to store calibration k in eeprom
  ph.begin();
  ec.begin();
  sensors.begin();


  timer.setInterval(1000L,MainFunction);
}

void loop()
{

    // Blynk.run();
    timer.run(); // Initiates BlynkTimer
    

}

void MainFunction()
{


    TDSvoltage = analogRead(A0); // A0 is the gpio 36
    Serial.print("TDSvoltage:");
    Serial.println(TDSvoltage, 4);
    
    phvoltage = analogRead(A3) / ESPADC * ESPVOLTAGE; // A3 is the gpio 39 
    Serial.print("phvoltage:");
    Serial.println(phvoltage, 4);

    temperature = readTemperature();  // read your temperature sensor to execute temperature compensation
    Serial.print("temperature:");
    Serial.print(temperature, 1); 
    Serial.println("^C");

    ecValue = ec.readEC(TDSvoltage, temperature); // convert voltage to EC with temperature compensation
    Serial.print("EC:");
    Serial.print(ecValue, 4);
    Serial.println("ms/cm");

    phValue = ph.readPH(phvoltage, temperature); // convert voltage to pH with temperature compensation
		Serial.print("pH:");
		Serial.println(phValue, 4);

    

// Sensor Values to Blynk application

  // Blynk.virtualWrite(V2, temperature);
  // Blynk.virtualWrite(V3, ecValue);

  ec.calibration(TDSvoltage, temperature);
  ph.calibration(phvoltage, temperature); // calibration process by Serail CMD

}