#include <SimpleTimer.h>

const int pHIncreasePin = 3;
const int pHDecreasePin = 5;
const int ECIncreasePin = 6;
const int ECIncreasePin2 = 9;
const int GrowLight = 10;

float pH_Value = 0.0;
int EC_Value = 0;
float target_pH = 0.0;
int target_EC = 0;
float pHError = 0.0;
float ECError = 0.0;
int target_GrowLight = 0;
// int Grow_Light_SetTimer = 0;
const float pH_Tolerance = 0.3;
const int EC_Tolerance = 50;

const unsigned long Dosing_interval = 500000;

SimpleTimer Dosing_pH_timer;
SimpleTimer Dosing_EC_timer;
SimpleTimer Timer;

void setup() {
  Serial.begin(115200);

  pinMode(pHIncreasePin, OUTPUT);
  pinMode(pHDecreasePin, OUTPUT);
  pinMode(ECIncreasePin, OUTPUT);
  pinMode(GrowLight, OUTPUT);

  Dosing_pH_timer.setInterval(Dosing_interval,Dosing_pH);
  Dosing_EC_timer.setInterval(Dosing_interval,Dosing_EC);
  // Thiết lập thời gian đầu tiên cho dosing

}

void loop() {
  receiveTargets();
  Timer.run();
  pHError = pH_Value - target_pH;
  ECError = EC_Value - target_EC;
  if (abs(pHError) > pH_Tolerance){
    Dosing_pH_timer.run();
  }
  if (abs(ECError) > EC_Tolerance){
    Dosing_EC_timer.run();
  }
}

void receiveTargets() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    int firstIndex = command.indexOf('/');
    int secondIndex = command.indexOf('/', firstIndex + 1);
    int thirdIndex = command.indexOf('/', secondIndex + 1);
    int GrowLightIndex = command.indexOf('/',thirdIndex+1);
    if (firstIndex >= 0 && secondIndex >= 0 && thirdIndex >= 0) {
      String pHValueString = command.substring(0, firstIndex);
      pH_Value = pHValueString.toFloat();

      String ECValueString = command.substring(firstIndex + 1, secondIndex);
      EC_Value = ECValueString.toInt();

      String targetValuesString = command.substring(secondIndex + 1, thirdIndex);
      target_pH = targetValuesString.toFloat();

      String targetECString = command.substring(thirdIndex + 1, GrowLightIndex);
      target_EC = targetECString.toInt();
    }


    if (GrowLightIndex >= 0) {
      String targetGrowLightString = command.substring(GrowLightIndex + 1);//, SetTimerIndex);
      target_GrowLight = targetGrowLightString.toInt();
      analogWrite(GrowLight,target_GrowLight*255/100);
    }

    // In giá trị pH, EC, target pH và target EC lên Serial Monitor
    Serial.print("pH Value: ");
    Serial.println(pH_Value, 2);
    Serial.print("EC Value: ");
    Serial.println(EC_Value);
    Serial.print("Target pH: ");
    Serial.println(target_pH, 2);
    Serial.print("Target EC: ");
    Serial.println(target_EC);
    Serial.print("Target Grow Light: ");
    Serial.println(target_GrowLight);
  }
}

void Dosing_pH(){
  if (pHError > 0) {
    digitalWrite(pHDecreasePin, HIGH);
    Timer.setTimeout(1000L, stop_pHDecrease);
  } else {
    digitalWrite(pHIncreasePin, HIGH);
    Timer.setTimeout(1000L, stop_pHIncrease);
  }
}

void Dosing_EC(){
  if (ECError > 0) {
    //nothing
  } else {
    digitalWrite(ECIncreasePin, HIGH);
    digitalWrite(ECIncreasePin2, HIGH);
    Timer.setTimeout(1000L, stop_ECIncrease);
  }
}

void stop_pHDecrease(){
  digitalWrite(pHDecreasePin, LOW);
}
void stop_pHIncrease(){
  digitalWrite(pHIncreasePin, LOW);
}
void stop_ECIncrease(){
  digitalWrite(ECIncreasePin, LOW);
  digitalWrite(ECIncreasePin2, LOW);
}
