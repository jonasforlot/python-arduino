#include "HX711.h"
 
HX711 capteur;
int DAT = 3;
int CLK = 2;
long valeur;
float valeur2;
 
void setup() {
  pinMode(8,OUTPUT);
  digitalWrite(8,HIGH); // crée une alimenatation 5V sur la broche 8
  capteur.begin(DAT, CLK);
  Serial.begin(9600);
  while (!Serial) {
  }
 Serial.print("Capteur ");
 Serial.println("HX711");
  // tarage du capteur
  Serial.println("Tarage du capteur");
  Serial.println("Le capteur doit être fixé et ne pas être touché ou déplacé");
  capteur.tare();
  delay(1000);
}
 
void loop() {
  valeur = capteur.get_value();
  valeur2 = 0.00234*valeur -0.328 ;
  Serial.print("Valeur mesurée (avec tare) : ");
  Serial.print(valeur);
  Serial.println ("\t");
  Serial.println(valeur2);
  delay(20);
  
}
