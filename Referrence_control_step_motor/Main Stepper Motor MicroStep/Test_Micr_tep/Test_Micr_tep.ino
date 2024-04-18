#define out1  11
#define out2 10
#define out3 9
#define out4 8
#define enA 5
#define enB 6 
#define BTMain 12
#define BT6 1
#define BT5 0
#define BT3 7
#define BT4 3
const int RedLed = 2;
const int YellowLed = 4;
float PWM1,PWM2=0;
long int v =10,v1,v2;
int i=0,u=0, TT=0;
float dl;
float x=16;
signed int s,h=0;
signed int S1_state=0;
const unsigned char MicroStep1[16]={24.99,51,73.95,96.9,119.85,142.8,160.65,181.05,196.35,211.65,224.4,237.15,243.78,249.9,253.725,255};
const unsigned char MicroStep2[16]={253.725,249.9,243.78,237.15,224.4,211.65,196.35,181.05,160.65,142.8,119.85,96.9,73.95,51,24.99,0};
void setup() {
  // put your setup code here, to run once:
  pinMode(out1, OUTPUT);
  pinMode(out2, OUTPUT);
  pinMode(out3, OUTPUT);
  pinMode(out4, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(enB , OUTPUT);
  pinMode(BTMain,INPUT_PULLUP);
  pinMode(BT3,INPUT_PULLUP);
  pinMode(BT4,INPUT_PULLUP);
  pinMode(BT5,INPUT_PULLUP);
  pinMode(BT6,INPUT_PULLUP);
  pinMode(RedLed, OUTPUT);
  pinMode(YellowLed, OUTPUT);
  digitalWrite(out3,LOW);
  digitalWrite(out2,LOW);
  digitalWrite(out1,LOW);
  digitalWrite(out4,LOW);
  digitalWrite(RedLed,LOW);
  digitalWrite(YellowLed,LOW);
  Serial.begin(9600);
}

void delay()
{
  v1 = v*200;  //So step quay trong 1 phut
  v2 = v1/60;  //Toc do dong co(v/p)
 dl = 1000/v2; //1000ms = 1s  
}

void tien_micro_step(){   //chia 16 (N=16)
  PWM1=0;PWM2=255;
  for(int i = 0; i <=3; i++){
       delay();
     if(digitalRead(BT6)== 0)          // Velocity control
      {
        delay(20);
        while(digitalRead(BT6)== 0){}
            h++;
            if(h>2)h=0;
            if (h==0)x=16;
            if (h==1) x=8;
            if (h==2) x=4;
    }
       if(i==0) {
          digitalWrite(out4,LOW);
          digitalWrite(out3,HIGH);
          digitalWrite(out2,LOW);
          digitalWrite(out1,HIGH);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==1) {
          digitalWrite(out4,LOW);
          digitalWrite(out3,HIGH);
          digitalWrite(out2,HIGH);
          digitalWrite(out1,LOW);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==2) {
            digitalWrite(out4,HIGH);
            digitalWrite(out3,LOW);
            digitalWrite(out2,HIGH);
            digitalWrite(out1,LOW);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==3) {
            digitalWrite(out4,HIGH);
            digitalWrite(out3,LOW);
            digitalWrite(out2,LOW);
            digitalWrite(out1,HIGH);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
  }
}

void lui_micro_step(){   //chia 16 (N=16)
  PWM1=0;PWM2=255;
  for(int i = 0; i <=3; i++){
       delay();
     if(digitalRead(BT6)== 0)          // Velocity control
      {
        delay(20);
        while(digitalRead(BT6)== 0){}
            h++;
            if(h>2)h=0;
            if (h==0)x=16;
            if (h==1) x=8;
            if (h==2) x=4;
    }
       if(i==0) {
          digitalWrite(out1,LOW);
          digitalWrite(out2,HIGH);
          digitalWrite(out3,LOW);
          digitalWrite(out4,HIGH);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==1) {
          digitalWrite(out1,LOW);
          digitalWrite(out2,HIGH);
          digitalWrite(out3,HIGH);
          digitalWrite(out4,LOW);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==2) {
            digitalWrite(out1,HIGH);
            digitalWrite(out2,LOW);
            digitalWrite(out3,HIGH);
            digitalWrite(out4,LOW);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
      if(i==3) {
            digitalWrite(out1,HIGH);
            digitalWrite(out2,LOW);
            digitalWrite(out3,LOW);
            digitalWrite(out4,HIGH);
          for (int z=0; z<=15 ; z++){
            PWM1=MicroStep1[z];
            PWM2=MicroStep2[z];
            analogWrite(enA,PWM1);
            analogWrite(enB,PWM2);
            delay(float(dl/x));}
      }
  }
}


void loop() {
  // put your main code here, to run repeatedly:
  if ((S1_state == 0) && (digitalRead(BTMain) == 1)) S1_state =1;
  if ((S1_state == 1) && (digitalRead(BTMain) == 0)) S1_state =2;
  if ((S1_state == 2) && (digitalRead(BTMain) == 1)) S1_state =3;
  if ((S1_state == 3) && (digitalRead(BTMain) == 0)) S1_state =4;
  if ((S1_state == 4) && (digitalRead(BTMain) == 1)) S1_state =5;
  if ((S1_state == 5) && (digitalRead(BTMain) == 0)) S1_state =6;
  if ((S1_state == 6) && (digitalRead(BTMain) == 1)) S1_state =1;

  if (S1_state==1){
    digitalWrite(RedLed,LOW);
    digitalWrite(YellowLed,LOW);
    TT=0;
  }
  if (S1_state==3){
    if(digitalRead(BT5)==0)
    {
      digitalWrite(RedLed,HIGH);
      digitalWrite(YellowLed,LOW);
      delay(500);
      TT=0;
      u=0;
    }
    if(digitalRead(BT3)==0)
    {
      while(digitalRead(BT3)== 0){}
      TT=1;
      u=0;
    }
    if(digitalRead(BT4)==0)
    {
      while(digitalRead(BT4)== 0){}
      TT=2;
      u=0;
    }
    if(TT==1)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<100)
      {
        tien_micro_step();
        u++;
        delay(s);
      }
    }
    if(TT==2)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<42)
      {
        lui_micro_step();
        u++;
        delay(s);
      }
    }
      
  }
  if (S1_state==5){    // Normal Control
    if(digitalRead(BT5)==0)
    {
      digitalWrite(RedLed,HIGH);
      digitalWrite(YellowLed,LOW);
      TT=0;
      u=0;
    }
    if(digitalRead(BT3)==0)
    {
      while(digitalRead(BT3)== 0){}
      TT=1;
      u=0;
    }
    if(digitalRead(BT4)==0)
    {
      while(digitalRead(BT4)== 0){}
      TT=2;
      u=0;
    }
    if(TT==1)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==1)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT4)==0 || digitalRead(BT6)==0 ){break;}
        tien_micro_step();
      }
    }
    if(TT==2)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==2)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT3)==0 || digitalRead(BT6)==0 ){break;}
        lui_micro_step();
      }
    }
      }
 }
