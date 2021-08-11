
#include "QGPMaker_MotorShield.h"
#include <Wire.h>
#include <SPI.h>

QGPMaker_MotorShield AFMS = QGPMaker_MotorShield();
QGPMaker_DCMotor *DCMotor_1 = AFMS.getMotor(1);
QGPMaker_DCMotor *DCMotor_2 = AFMS.getMotor(2);
QGPMaker_DCMotor *DCMotor_3 = AFMS.getMotor(3);
QGPMaker_DCMotor *DCMotor_4 = AFMS.getMotor(4);

int Clockwise_Rotation_Pin = 6;        //顺时针旋转引脚
int Counter_Clockwise_Rotation_pin = 7;//逆时针旋转引脚
int Turn_Right_pin = 4;                //右平移引脚
int Turn_Left_pin = 5;                 //左平移引脚
int Forward_pin = 2;                   //前进引脚
int Back_pin = 3;                      //后进引脚

int gpio_state(int f_state, int b_state, int r_state, int l_state, int s_state, int n_state)
{
  if (f_state == digitalRead(2) && b_state == digitalRead(3) &&
      r_state == digitalRead(4) && l_state == digitalRead(5) &&
      s_state == digitalRead(6) && n_state == digitalRead(7) ) {
    return 1;
  }
  else {
    return 0;
  }
}

int Flag = 0;
float n = 1.40625;
float yaw,target_yaw;
volatile boolean received;
float Max_error = 5.0;
byte Rotation_flag = 1;

void setup()
{
  Serial.begin(115200);
  AFMS.begin(50);

  pinMode(Clockwise_Rotation_Pin, INPUT);
  pinMode(Counter_Clockwise_Rotation_pin, INPUT);
  pinMode(Turn_Right_pin, INPUT);
  pinMode(Turn_Left_pin, INPUT);
  pinMode(Forward_pin, INPUT);
  pinMode(Back_pin, INPUT);

  pinMode(MISO,OUTPUT); 
  SPCR |= _BV(SPE);
  received = false;
  SPI.attachInterrupt(); 
}

ISR(SPI_STC_vect)
{
  yaw = SPDR;
  received = true;
}

void loop()
{
  Serial.print("yaw1 = ");
  target_yaw = MAP(yaw);
  Serial.println(target_yaw);
  Serial.println(yaw);
//  Forward();
//  delay(5000);
//  Stop();
//  delay(2000);
//
//  Back();
//  delay(5000);
//  Stop();
//  delay(2000);
//
//  Turn_Right();
//  delay(2000);
//  Stop();
//  delay(2000);
//
//  Turn_Left();
//  delay(2000);
//  Stop();
//  delay(2000);
  
  if (gpio_state(1, 0, 1, 0, 1, 0))
  {
    Flag = 1;
  }
  
  if (Flag == 1)
  //if (0)
  {
    if (gpio_state(0, 0, 0, 0, 1, 0)) //00 0010
    {
      Clockwise_Rotation();
    }
    else if (gpio_state(0, 0, 0, 0, 0, 1)) //00 0001
    {
      Counter_Clockwise_Rotation();
    }
    else if (gpio_state(0, 0, 1, 0, 0, 0)) //00 1000
    {
      Turn_Right();
    }
    else if (gpio_state(0, 0, 0, 1, 0, 0)) //00 0100
    {
      Turn_Left();
    }
    else if (gpio_state(1, 0, 0, 0, 0, 0)) //10 0000
    {
      Forward();
    }
    else if (gpio_state(0, 1, 0, 0, 0, 0)) //01 0000
    {
      Back();
    }
    else if (gpio_state(0, 1, 0, 1, 0, 1)) //01 0101
    {
      Flag = 0;
      Stop();
    }
    else if(gpio_state(0, 0, 0, 0, 0, 0))
    {
      Stop();
    } 
  }
  else
  {
    Stop();
  }
  
  //Stop();
    
    if(Rotation_flag == 1)
    {
      Serial.print("======");
      if(target_yaw < Max_error && target_yaw > -Max_error)
      {
         Rotation_flag = 0;
        
      }
      else if(target_yaw >= Max_error)
      {
        Serial.print("------");
        //Clockwise_Rotation();
      }
      else if(target_yaw <= -Max_error)
      {
        //Counter_Clockwise_Rotation();
      }
    }
}

float MAP(float dat)
{
  float x = 0.0;
  x = 180.0 - dat * n;
  return x;
}

void Forward() //前进
{
  Serial.println("前进");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(82);
  DCMotor_4->setSpeed(78);
  DCMotor_1->run(BACKWARD);
  DCMotor_2->run(FORWARD);
  DCMotor_3->run(FORWARD);
  DCMotor_4->run(BACKWARD);
}

void Back() //后退
{
  Serial.println("后退");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(82);
  DCMotor_4->setSpeed(78);
  DCMotor_1->run(FORWARD);
  DCMotor_2->run(BACKWARD);
  DCMotor_3->run(BACKWARD);
  DCMotor_4->run(FORWARD);
}

void Turn_Right() //右平移
{
  Serial.println("右移");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(78);
  DCMotor_4->setSpeed(75);
  DCMotor_1->run(FORWARD);
  DCMotor_2->run(FORWARD);
  DCMotor_3->run(BACKWARD);
  DCMotor_4->run(BACKWARD);
}

void Turn_Left() //左平移
{
  Serial.println("左移");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(78);
  DCMotor_4->setSpeed(75);
  DCMotor_1->run(BACKWARD);
  DCMotor_2->run(BACKWARD);
  DCMotor_3->run(FORWARD);
  DCMotor_4->run(FORWARD);
}

void Clockwise_Rotation() //顺时针旋转
{
  Serial.println("顺");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(82);
  DCMotor_4->setSpeed(78);
  DCMotor_1->run(FORWARD);
  DCMotor_2->run(FORWARD);
  DCMotor_3->run(FORWARD);
  DCMotor_4->run(FORWARD);
}

void Counter_Clockwise_Rotation() //逆时针旋转
{
  Serial.println("逆");
  DCMotor_1->setSpeed(98);
  DCMotor_2->setSpeed(83);
  DCMotor_3->setSpeed(82);
  DCMotor_4->setSpeed(78);
  DCMotor_1->run(BACKWARD);
  DCMotor_2->run(BACKWARD);
  DCMotor_3->run(BACKWARD);
  DCMotor_4->run(BACKWARD);
}

void Stop() //小车停止
{
  Serial.println("stop");
  DCMotor_1->setSpeed(0);
  DCMotor_1->run(RELEASE);
  DCMotor_2->setSpeed(0);
  DCMotor_2->run(RELEASE);
  DCMotor_3->setSpeed(0);
  DCMotor_3->run(RELEASE);
  DCMotor_4->setSpeed(0);
  DCMotor_4->run(RELEASE);
  Rotation_flag = 1;
}
