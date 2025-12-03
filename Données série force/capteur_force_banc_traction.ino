// En sortie filtre passe bas R = 47 kOhms, C = 10 microF

#include "HX711.h"

HX711 capteur;
int DAT = 3;
int CLK = 2;

long valeur;
float valeur2;

int pinPWM = 9;  // Pin PWM vers filtre RC puis A0 de l’autre Arduino

void setup() {
  capteur.begin(DAT, CLK);
  Serial.begin(9600);
  capteur.tare();
  delay(1000);
}

void loop() {
  valeur = capteur.get_value();
  valeur2 = 0.00234 * valeur - 0.328;   // ta conversion en grammes

  // Conversion -5000…5000 g -> PWM 0…255
  int sortiePWM = map(valeur2, -5000, 0, 255, 0);
  sortiePWM = constrain(sortiePWM, 0, 255);

  analogWrite(pinPWM, sortiePWM); // PWM vers filtre RC

  // debug
  Serial.println(valeur2);
    Serial.println(sortiePWM);

  

  delay(20);
}
