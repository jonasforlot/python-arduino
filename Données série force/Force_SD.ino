#include "HX711.h"
#include <SPI.h>
#include <SD.h>

#include <Wire.h>
 HX711 capteur;
 int DAT = 3;
 int CLK = 2;
 long valeur;
 float valeur2;
 
long temps;
File fichierSD;

 void setup() {
//  pinMode(8,OUTPUT);
 //  digitalWrite(8,HIGH); // si on veut créer une alimentation 5V sur la broche 8 de la carte Arduino, pour la broche VDD de l'amplificateur
   capteur.begin(DAT, CLK);
//   Serial.begin(9600);
//   while (!Serial) {
//   }
//  Serial.print("Capteur ");
//  Serial.println("HX711");
//   // tarage du capteur
//   Serial.println("Tarage du capteur");
//   Serial.println("Le capteur doit être fixé et ne pas être touché ou déplacé");
   capteur.tare();
   delay(1000);
   //  Initialisation de la carte SD
    if(!SD.begin(10)) {
//      Serial.println(F("Initialisation SD impossible !"));
    return;
    }
    
 }
 void loop() {
   fichierSD = SD.open("force.txt", FILE_WRITE);
 
   temps = millis();
   valeur = capteur.get_value();
   valeur2 = 0.00234*valeur -0.328 ;
//   Serial.print("Valeur mesurée (avec tare) : ");
//   Serial.print(temps);
//   Serial.println ("\t");
//   Serial.println(valeur2);

    if(fichierSD) {
    //     Serial.println(F("Ecriture en cours"));
   //Ecriture
      fichierSD.print(temps);
  
    fichierSD.print("\t");
    fichierSD.print(valeur2);
    fichierSD.println(""); 

    fichierSD.close();
  }
   delay(50);
 }
