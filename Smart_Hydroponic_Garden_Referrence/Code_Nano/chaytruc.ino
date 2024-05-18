//100xung -> 20mm
//50 xung -> 10mm
//base x 1.5
// base y 5.5

#include <AccelStepper.h>
#include <MultiStepper.h>

const int limitX = 9;  // Chân D9 kết nối với công tắc hành trình trục X
const int limitY = 10; // Chân D10 kết nối với công tắc hành trình trục Y

// Khai báo đối tượng AccelStepper cho trục X và Y
AccelStepper stepperX(AccelStepper::DRIVER, 5, 2); // Chân STEP và DIR của trục X kết nối với chân D2 và D5 trên Arduino
AccelStepper stepperY(AccelStepper::DRIVER, 6, 3); // Chân STEP và DIR của trục Y kết nối với chân D3 và D6 trên Arduino
MultiStepper multiStepper;

long targetX[19]={150,150,150,150,150,150,
                1050,1050,1050,1050,1050,1050,1050,
                1925,1925,1925,1925,1925,1925};
long targetY[19]={600,1350,2100,2875,3600,4375,
                100,825,1600,2325,3075,3850,4600,
                600,1275,2050,2775,3600,4300};

void setup() {
  // Khởi động kết nối Serial Monitor
  Serial.begin(115200);
  // Thiết lập chân công tắc hành trình là INPUT_PULLUP
  pinMode(limitX, INPUT_PULLUP);
  pinMode(limitY, INPUT_PULLUP);

  stepperX.setEnablePin(8); // chon enable pin 8 ( X,Y dung chung enable)
  stepperX.setPinsInverted(true,false,true); // dao nguoc chan enable

  stepperX.setMaxSpeed(800); // Tốc độ tối đa trục X (đơn vị: steps/s)
  stepperX.setAcceleration(6000); // Gia tốc trục X (đơn vị: steps/s^2)

  stepperY.setMaxSpeed(800); // Tốc độ tối đa trục Y (đơn vị: steps/s)
  stepperY.setAcceleration(6000); // Gia tốc trục Y (đơn vị: steps/s^2)

  multiStepper.addStepper(stepperX);
  multiStepper.addStepper(stepperY);
  
  SetHome();
}

void loop() {
  
  if (Serial.available()) {  // Kiểm tra xem có dữ liệu có sẵn để đọc từ UART hay không
    stepperX.enableOutputs();
    String data = Serial.readString();
    //Serial.print("Go to position: ");
    //Serial.println(data);
    int pos = data.toInt();
    if(pos !=0){
      String data_trans =  (String) pos;
      gotoXY(pos);
      delay(500);
      stepperX.disableOutputs();
      // if(pos==11){
      //   Serial.print("01");  
      // }else{
      //   Serial.print(data_trans);
      // }
      Serial.println(data_trans);
    }
    else {
      SetHome() ;
      // Serial.print("0");
    }
  }
}

void SetHome()
{
  stepperX.enableOutputs();
  
  while(digitalRead(limitX)==HIGH)
    {
      stepperX.setSpeed(-800);
      stepperX.runSpeed(); // Di chuyển trục X
    }
  stepperX.setCurrentPosition(0);
  delay(500);
  while(digitalRead(limitY)==HIGH)
    {
      // Serial.println(digitalRead(limitY));
      stepperY.setSpeed(-800);
      stepperY.runSpeed(); // Di chuyển trục X
    }
  stepperY.setCurrentPosition(0);
  delay(1000);
  stepperX.disableOutputs();
  
}

void gotoXY(int pos){
  stepperX.moveTo(targetX[pos-1]); // Đặt vị trí home trục X
  stepperY.moveTo(targetY[pos-1]); // Đặt vị trí home trục Y
  while(stepperX.distanceToGo() != 0 ||stepperY.distanceToGo() != 0)  
  {
    stepperX.run();
    stepperY.run();
  }
}