#include <Servo.h>

Servo servoEO;
Servo servoNS;

void setup() {

  servoEO.attach(9);
  servoNS.attach(10);

  // Position centrale des deux servomoteurs
  servoEO.write(90);
  servoNS.write(90);
}

void loop() {
  // Les servomoteurs restent à 90°

}
