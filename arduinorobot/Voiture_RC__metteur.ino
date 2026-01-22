#include <SoftwareSerial.h>

// Broches pour le joystick GT1079
int joystick_x_pin = A0;
int joystick_y_pin = A1;

SoftwareSerial BTSerial(12, 13); // RX, TX pour le module HC-05

void setup() {
  Serial.begin(9600); // Initialisation de la communication série avec le moniteur série
  BTSerial.begin(9600); // Initialisation de la communication série avec le module HC-05
}

void loop() {
  int x_val = analogRead(joystick_x_pin); // Lire la valeur de l'axe X du joystick
  int y_val = analogRead(joystick_y_pin); // Lire la valeur de l'axe Y du joystick

  // Affichage des valeurs des axes X et Y dans le moniteur série
//  Serial.print("X : ");
  Serial.print(x_val);
 Serial.print("\t");
  Serial.println(y_val);

  // Envoi des valeurs des axes X et Y au module HC-05
  BTSerial.print(x_val);
  BTSerial.print("\t");
  BTSerial.println(y_val);

  delay(100); // Délai pour éviter une lecture trop rapide du joystick
}
