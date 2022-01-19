/* 
 * Code pour compteur de défilement d'anneaux avevl'interféromètre de Michelson.
 * Un photodétecteur (« cible » DIDALAB par exemple) est connecté à la première entrée analogique 
 * (entrée A1 car AO est déjà utilisée pour récupérer les valeurs envoyées par les boutons du curseur du shield).

  Le réglage du seuil de détection dépend du photodétecteur et de la luminosité. Idéalement, 
  il faudrait qu’il corresponde à la valeur moyenne de la tension mesurée lors de l’alternance des franges ou anneaux. 
  Pour le régler efficacement, il suffit de faire défiler les anneaux en maintenant le bouton  RIGHT enfoncé, 
  ou faire une acquisition avec la carte Sysam pour visualiser la tension.
.
 */

#include <EEPROM.h>

#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9, 4, 5, 6, 7);
int sensor = A1; // broche pour détection du capteur
int etatSensor ; // état du capteur (haut ou bas)
int valeur_bouton;
int seuil  ;
float seuil_tension ;
int mesure;
int somme_mesure = 0;
float mesure_tension;
float valeur_moyenne =0;
int compt_moy = 0;
bool etat_old= false ; // 
bool  etat_new = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
int compt=0; // comptage initialisé à 0
long temps; //mesure du temps pour l'acquisition

void setup() 
{
  
  Serial.begin(9600); // pour le moniteur série
  lcd.begin(16,2);
  int seuil;
  valeur_bouton  = analogRead(A0);
  temps = millis();
}  
 
void loop()
{

valeur_bouton  = analogRead(A0);
//Serial.println(valeur_bouton);

// gestion des boutons du curseur 
//(remise à zéro pour LEFT, réglage du seuil auto avec RIGHT,
//réglage du seui manuel avec UP/DOWN)

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
  somme_mesure = 0;
  compt_moy = 0;
  delay(100);
}

temps = millis();
mesure = analogRead(sensor);
mesure_tension = mesure*5.0/1023;
seuil_tension = seuil *5.0/1023;

if (valeur_bouton == 0) {
  
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(" Etalonnage  ");
  lcd.setCursor(0,1);
  lcd.print("Chariotter SVP");
 
  compt_moy = compt_moy + 1;
  somme_mesure = somme_mesure + mesure;
  valeur_moyenne = somme_mesure/compt_moy;
  seuil = valeur_moyenne;
  EEPROM.put(0, seuil);
//  Serial.print(compt_moy);
//Serial.print ("\t");
//Serial.println(valeur_moyenne);
  delay(500);
 lcd.clear();
  
}
else{
  somme_mesure = 0;
  compt_moy = 0;
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
//  
Serial.print(temps);
Serial.print ("\t");
Serial.println(mesure_tension);

//Serial.println(valeur_bouton);

 delay(20);
}
