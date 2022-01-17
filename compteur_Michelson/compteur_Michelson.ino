#include <EEPROM.h>

#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);
int sensor = A1; // broche pour détection du capteur
int etatSensor ; // état du capteur (haut ou bas)
int valeur_bouton;
int seuil  ;
float seuil_tension ;
int mesure;
float mesure_tension;

bool etat_old= false ; // 
bool  etat_new = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
int compt=0; // comptage initialisé à 0
long temps; //mesure du temps pour l'acquisition

void setup() 
{
  
  Serial.begin(9600); // pour le moniteur série
  lcd.begin(16,2);
  int seuil;
 
  temps = millis();
}  
 
void loop()
{

valeur_bouton  = analogRead(A0);
Serial.println(valeur_bouton);


if (valeur_bouton ==205 or valeur_bouton ==203) {
  seuil+=1;
  EEPROM.put(0, seuil);
  delay(10);
}
if (valeur_bouton == 405 or valeur_bouton == 402) {
  seuil-=1;
  EEPROM.put(0, seuil);
  delay(10);
}

 EEPROM.get(0,seuil);
 
if (valeur_bouton == 619 or valeur_bouton == 622) {
  lcd.clear();
  compt=0;
  delay(100);
}

temps = millis();
mesure = analogRead(sensor);
mesure_tension = mesure*5.0/1023;
seuil_tension = seuil *5.0/1023;

if (valeur_bouton == 0) {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Valeur tension  ");
  lcd.setCursor(5,1);
  lcd.print(mesure_tension);
  lcd.print(" V");
  delay(1000);
  lcd.clear();
}

lcd.setCursor(0,0);
lcd.print("Comptage  |seuil");
lcd.setCursor(0,1);
lcd.print(compt/2);
lcd.setCursor(10,1);
lcd.print("|");
lcd.setCursor(11,1);
lcd.print(seuil_tension);
lcd.setCursor(15,1);
lcd.print("V");



if (mesure_tension> seuil_tension){
  etat_new = true; 
}
else {
  etat_new =false;
}
if (etat_old != etat_new) {
  etat_old = etat_new;
  compt = compt + 1;
//  Serial.print("  comptage ");
//  Serial.println(compt);
//lcd.clear();






  }
  
Serial.print(temps);
Serial.print ("\t");
Serial.println(mesure_tension);

//Serial.println(valeur_bouton);

 delay(10);
}
