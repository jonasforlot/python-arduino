#include <EEPROM.h>
#include "Ultrasonic.h"
#include <LiquidCrystal.h>

LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
int sensor = A1; // broche pour détection du capteur
int etatSensor; // état du capteur (haut ou bas)
long RangeInCentimeters;
int valeur_bouton;
int attente;
int periode = 20000; // période entre chaque début d'impulsion en microsecondes
int pinServo = 0; // variable pour le pin connecté à la commande du servo
bool state = false;
bool etat_reglage = false;

Ultrasonic ultrasonic(16);

//*******************************************************************************//
// Association des entrées du L298N, aux sorties utilisées sur notre Arduino Uno //
//*******************************************************************************//
#define borneENA 11  // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1 12  // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2 13  // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3 1   // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4 2   // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB 3   // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
int PWM = 50; // Variable PWM image de la vitesse

//*******//
// SETUP //
//*******//
void setup() {
  EEPROM.get(0,attente);
  valeur_bouton  = analogRead(A0);
  lcd.begin(16,2);
  if (valeur_bouton == 619 or valeur_bouton ==620) {
    etat_reglage = true;
 
    while (etat_reglage == true){
      if ((valeur_bouton != 820 and valeur_bouton != 821 )) {
        lcd.setCursor(0,0);
        lcd.print("tps|Select");
        
        lcd.setCursor(3,1);
        lcd.print("|");
        lcd.setCursor(4,1);
        lcd.print("pour valider");
        
        delay(100);
        valeur_bouton  = analogRead(A0);
        
        
    
        if (valeur_bouton ==205 or valeur_bouton ==203 or valeur_bouton ==204) {
      attente+=1;
      EEPROM.put(0, attente);
      delay(100);
    }
    if (valeur_bouton == 405 or valeur_bouton == 402 or valeur_bouton == 401) {
      attente-=1;
      EEPROM.put(0, attente);
      delay(100);
    }
        lcd.clear();
        lcd.setCursor(0,1);
        lcd.print(attente);
        
      }
    
      else{
         
        etat_reglage = false;
      }
    }
  }
  lcd.clear();
  
  pinMode(16, INPUT);
  pinMode(pinServo, OUTPUT); // on prépare le pin en mode OUTPUT
  digitalWrite(pinServo, LOW); // on l'initialise à l'état bas

  delay(50);

  lcd.begin(16, 2); // utilisation d'un écran 16 colonnes et 2 lignes
  lcd.setCursor(0, 0);
  lcd.write("Rock Star ready");
  lcd.setCursor(0, 1);
  lcd.write("for the show !");
  
  
  // Tant que la distance mesurée est inférieure à 10 cm, attendre
  while (analogRead(A1) > 100) {
    delay(100); // Attente avant de vérifier à nouveau
  }

  // Configuration des moteurs en marche avant
 marche_avant();

  // Compte à rebours de 5 secondes
  for (int i = attente; i > 0; i--) {
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Compte a rebours :");
    lcd.setCursor(0, 1);
    lcd.print(i);
    delay(1000);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   Let's Rock !");
  

  // Lancer les moteurs
  analogWrite(borneENA, 80);
  analogWrite(borneENB, 80);
  delay (100);
  analogWrite(borneENA, 50);
  analogWrite(borneENB, 50);
  delay (300);
  analogWrite(borneENA, 30);
  analogWrite(borneENB, 30);
  delay (300);
  arret();
  delay (500);

  marche_avant;
  analogWrite(borneENA, 0);
  analogWrite(borneENB, 100);
  delay (100);
  analogWrite(borneENA, 0);
  analogWrite(borneENB, 60);
  delay (400);
  arret();
  delay (500);

  marche_avant();
  analogWrite(borneENA, 70);
  analogWrite(borneENB, 70);
  
  delay(200);
  analogWrite(borneENA, 20);
  analogWrite(borneENB, 20);
  

  

  unsigned long startTime = millis();
  while (millis() - startTime < 3000) { // Boucle pendant 3 secondes
    int distance = mesure_US(); // Mesure la distance
    if (distance > 3) { // Si la distance est supérieure à 3 cm
      // Arrêt immédiat des moteurs
      arret();
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Bord de scene!");
      delay(2000); // Temps pour afficher le message
      break; // Sort de la boucle
    }
  }

  arret();
 
  state = true;
  while (true) {
    fete();
  }
}

void loop() {
  // Rien à exécuter ici pour l'instant
}

void fete() {
  setAngle(0);
  delayMicroseconds(1500);
  setAngle(90);
  delayMicroseconds(1500);
}

// Fonction setAngle pour envoyer les impulsions
void setAngle(int a) {
  int duree = map(a, 0, 179, 1000, 2000);
  digitalWrite(pinServo, LOW);

  for (int t = 0; t < 300; t++) {
    digitalWrite(pinServo, HIGH);
    delayMicroseconds(duree);
    digitalWrite(pinServo, LOW);
    delayMicroseconds(periode - duree);
  }
}

int mesure_US() {
  RangeInCentimeters = ultrasonic.MeasureInCentimeters();
  lcd.setCursor(0, 1);
  lcd.print("distance sol:");
  lcd.setCursor(14, 1);
  lcd.print(RangeInCentimeters);
  delay(250);
  return RangeInCentimeters;
}

void arret(){
   // Arrêt des moteurs après la période (si aucun obstacle)
  digitalWrite(borneIN1, LOW);
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, LOW);
  digitalWrite(borneIN4, LOW);
  analogWrite(borneENB, 0);
  analogWrite(borneENA, 0);
}

void marche_avant(){
   // Configuration des moteurs en marche avant
  digitalWrite(borneIN1, HIGH);
  digitalWrite(borneIN2, LOW);
  digitalWrite(borneIN3, HIGH);
  digitalWrite(borneIN4, LOW);
}
