#include<Servo.h>

Servo serX;
Servo serY;

String Data;

void setup() {

  serX.attach(7);
  serY.attach(10);
  Serial.begin(9600);
  Serial.setTimeout(10);
}

void loop() {
  //unrequired but necessary
}

void serialEvent() {
  Data = Serial.readString();
  serX.write(parseX(Data));
  serY.write(parseY(Data));
}

int parseX(String data){
  data.remove(data.indexOf("Y"));
  data.remove(data.indexOf("X"), 1);
  return data.toInt();
}

int parseY(String data){
  data.remove(0,data.indexOf("Y") + 1);
  return data.toInt();
}
