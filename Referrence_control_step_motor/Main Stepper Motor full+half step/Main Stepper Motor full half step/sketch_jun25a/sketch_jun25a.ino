#include <stdio.h>
#define BT1 13   //NGUOCCHIEUKDH
#define BT2 A0  //CUNGCHIEUKDH
#define BT3 7
#define BT4 3
#define BT5 0
#define BT6 1
#define BTMain 12
#define enA 5
#define enB 6
//const unsigned char MicroStep1[16] = {24.99,51,73.95,96.9,119.85,142.8,160.65,181.05,196.35,211.65,224.4,237.15,243.78,249.9,253.725,255};
//const unsigned char MicroStep2[16] = {253.725,249.9,243.78,237.15,224.4,211.65,196.35,181.05,160.65,142.8,119.85,96.9,73.95,51,24.99,0};
const int out1 = 8;
const int out2 = 9;
const int out3 = 10;
const int out4 = 11;
const int RedLed = 2;
const int YellowLed = 4;
int i=0,u=0, TT=0;
float dl;
signed int s,h=0;
signed int S1_state=0;
long int v =110,v1,v2;
float PWM1,PWM2=0;

void setup() {
pinMode(BT1,INPUT_PULLUP);
pinMode(BT2,INPUT_PULLUP);
pinMode(BT3,INPUT_PULLUP);
pinMode(BT4,INPUT_PULLUP);
pinMode(BT5,INPUT_PULLUP);
pinMode(BT6,INPUT_PULLUP);
pinMode(BTMain,INPUT_PULLUP);
pinMode(RedLed, OUTPUT);
pinMode(YellowLed, OUTPUT);
pinMode(out3, OUTPUT);
pinMode(out2, OUTPUT);
pinMode(out1, OUTPUT);
pinMode(out4, OUTPUT);
pinMode(enA, OUTPUT);
pinMode(enB, OUTPUT);
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

void tien_full_step()
{
  analogWrite(enA,255);
  analogWrite(enB,255);
for(int i = 0; i <=3; i++)
  {
  delay();
    if(i==0)      { digitalWrite(out4,LOW);digitalWrite(out3,LOW);digitalWrite(out2,LOW);digitalWrite(out1,HIGH);delay(dl);  }
    else if(i==1) { digitalWrite(out4,LOW);digitalWrite(out3,HIGH);digitalWrite(out2,LOW);digitalWrite(out1,LOW);delay(dl);  }
    else if(i==2) { digitalWrite(out4,LOW);digitalWrite(out3,LOW);digitalWrite(out2,HIGH);digitalWrite(out1,LOW);delay(dl);  }
    else if(i==3) { digitalWrite(out4,HIGH);digitalWrite(out3,LOW);digitalWrite(out2,LOW);digitalWrite(out1,LOW);delay(dl);  }
  }
}

void lui_full_step()
{
    analogWrite(enA,255);
    analogWrite(enB,255);
for(int i = 0; i <=3; i++)
  {
    delay();
    if(i==0) { digitalWrite(out4,HIGH);digitalWrite(out3,LOW);digitalWrite(out2,LOW);digitalWrite(out1,LOW);delay(dl);  }
    else if(i==1) { digitalWrite(out4,LOW);digitalWrite(out3,LOW);digitalWrite(out2,HIGH);digitalWrite(out1,LOW);delay(dl);  }
    else if(i==2) { digitalWrite(out4,LOW);digitalWrite(out3,HIGH);digitalWrite(out2,LOW);digitalWrite(out1,LOW);delay(dl);  }
    else if(i==3)      { digitalWrite(out4,LOW);digitalWrite(out3,LOW);digitalWrite(out2,LOW);digitalWrite(out1,HIGH);delay(dl);  }
  }
}

void tien_half_step()
 {
    analogWrite(enA,255);
    analogWrite(enB,255);
      for(int i = 0; i <=7; i++)
        {
          delay();
          if(i==0)      { digitalWrite(out1,LOW);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl);  }
          else if(i==1) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl); }
          else if(i==2) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,LOW);digitalWrite(out4,LOW);delay(dl);  }
          else if(i==3) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl); }
          else if(i==4) { digitalWrite(out1,LOW);digitalWrite(out2,LOW);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl);  }
          else if(i==5) { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl); }
          else if(i==6) { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,LOW);delay(dl);  }
          else if(i==7) { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl); }
        }
 }
void lui_half_step()
 {
    analogWrite(enA,255);
    analogWrite(enB,255);
    for(int i = 0; i <=7; i++)
      {
        delay();
             if(i==0)  { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl); }
         else if(i==1) { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,LOW);delay(dl);  }
         else if(i==2) { digitalWrite(out1,HIGH);digitalWrite(out2,LOW);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl); }
         else if(i==3) { digitalWrite(out1,LOW);digitalWrite(out2,LOW);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl);  }
         else if(i==4) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,HIGH);digitalWrite(out4,LOW);delay(dl); }
         else if(i==5) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,LOW);digitalWrite(out4,LOW);delay(dl);  }
         else if(i==6) { digitalWrite(out1,LOW);digitalWrite(out2,HIGH);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl); }
         else if(i==7) { digitalWrite(out1,LOW);digitalWrite(out2,LOW);digitalWrite(out3,LOW);digitalWrite(out4,HIGH);delay(dl);  }
      }
 }
void loop() {

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
  
  if (S1_state==3){    // Position Control
     if(digitalRead(BT6)== 0)          // Velocity control
    {
        delay(20);
        while(digitalRead(BT6)== 0){}
            h++;
            if(h>2)h=0;
            if (h==0) v=110;
            if (h==1) v=70;
            if (h==2) v=30;
    }
    if(digitalRead(BT5)==0)
    {
      while(digitalRead(BT5)== 0){}
      digitalWrite(RedLed,HIGH);
      digitalWrite(YellowLed,LOW);
      TT=0;
      u=0;
    }
    if(digitalRead(BT1)==0)
    {
      while(digitalRead(BT1)== 0){}
      TT=1;
      u=0;
    }
    if(digitalRead(BT2)==0)
    {
      while(digitalRead(BT2)== 0){}
      TT=2;
      u=0;
    }
    if(digitalRead(BT3)==0)
    {
      while(digitalRead(BT3)== 0){}
      TT=3;
      u=0;
    }
    if(digitalRead(BT4)==0)
    {
      while(digitalRead(BT4)== 0){}
      TT=4;
      u=0;
    }
    if(TT==1)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<300)
      {
        tien_full_step();
        u++;
        delay(s);
      }
    }
    if(TT==2)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<126)
      {
        lui_full_step();
        u++;
        delay(s);
      }
    }
      if(TT==3)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<300)
      {
        tien_half_step();
        u++;
        delay(s);
      }
    }
   if(TT==4)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      if(u<126)
      {
        lui_half_step();
        u++;
        delay(s);
      }
    }
  }
    if (S1_state==5){    // Normal Control
      if(digitalRead(BT6)== 0)          // Velocity control
    {
        delay(20);
        while(digitalRead(BT6)== 0){}
            h++;
            if(h>2)h=0;
            if (h==0)v=110;
            if (h==1) v=70;
            if (h==2) v=30;
    }
    if(digitalRead(BT5)==0)
    {
      while(digitalRead(BT5)== 0){}
      digitalWrite(RedLed,HIGH);
      digitalWrite(YellowLed,LOW);
      TT=0;
      u=0;
    }
    if(digitalRead(BT1)==0)
    {
      while(digitalRead(BT1)== 0){}
      TT=1;
      u=0;
    }
    if(digitalRead(BT2)==0)
    {
      while(digitalRead(BT2)== 0){}
      TT=2;
      u=0;
    }
    if(digitalRead(BT3)==0)
    {
      while(digitalRead(BT3)== 0){}
      TT=3;
      u=0;
    }
    if(digitalRead(BT4)==0)
    {
      while(digitalRead(BT4)== 0){}
      TT=4;
      u=0;
    }
    if(TT==1)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==1)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT2)==0 || digitalRead(BT3)==0 || digitalRead(BT4)==0 || digitalRead(BT6)==0 ){break;}
        tien_full_step();
        u++;
        delay(s);
      }
    }
    if(TT==2)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==2)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT1)==0 || digitalRead(BT3)==0 || digitalRead(BT4)==0 || digitalRead(BT6)==0 ){break;}
        lui_full_step();
        u++;
        delay(s);
      }
    }
      if(TT==3)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==3)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT2)==0 || digitalRead(BT1)==0 || digitalRead(BT4)==0 || digitalRead(BT6)==0 ){break;}
        tien_half_step();
        u++;
        delay(s);
      }
    }
   if(TT==4)
    {
      digitalWrite(RedLed,LOW);
      digitalWrite(YellowLed,HIGH);
      while(TT==4)
      {
        if(digitalRead(BT5)==0 || digitalRead(BT2)==0 || digitalRead(BT3)==0 || digitalRead(BT1)==0 || digitalRead(BT6)==0 ){break;}
        lui_half_step();
        u++;
        delay(s);
      }
    }
  }
}
