#include <ESP32Servo.h>

const int pin_servo_base = 18;
const int pin_servo_brazo_1 = 19;
const int pin_servo_brazo_2 = 21;
const int pin_servo_brazo_3 = 22;
const int pin_servo_agarre = 5;

byte angulos[5];

Servo servo_base;
Servo servo_1;
Servo servo_2;
Servo servo_3;
Servo servo_agarre;

void setup() {
  Serial.begin(115200);

  servo_base.attach(pin_servo_base);
  servo_1.attach(pin_servo_brazo_1);
  servo_2.attach(pin_servo_brazo_2);
  servo_3.attach(pin_servo_brazo_3);
  servo_agarre.attach(pin_servo_agarre);
  
}

void loop() {
  if (Serial.available()){
    int datos_recibidos = Serial.readBytes(angulos, 5);
    if(datos_recibidos == 5){
      servo_base.write(angulos[0]);
      servo_1.write(angulos[1]);
      servo_2.write(angulos[2]);
      servo_3.write(angulos[3]);
      servo_agarre.write(angulos[4]);
    }
  }
}
