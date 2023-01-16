// Adafruit Motor shield library
// copyright Adafruit Industries LLC, 2009
// this code is public domain, enjoy!

#include <AFMotor.h>

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
AF_Stepper motor(200, 2);

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  Serial.println("Stepper test!");

  motor.setSpeed(100);  // 100 rpm   
}

void loop() {
  Serial.println("Running clockwise");
  motor.step(200, FORWARD, SINGLE); 
  delay(1000);
  
  Serial.println("Running counter-clockwise");
  motor.step(400, BACKWARD, SINGLE); 
  delay(1000);
  

 
}
