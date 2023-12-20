#include "Wire.h"  // Arduino Wire library
#include "I2Cdev.h"  //bibliothèque I2Cdev à installer
#include "MPU6050.h" //bibliothèque MPU6050 à installer
MPU6050 accelgyro;

#define NOTE_F4  349
#define NOTE_G4  392
#define NOTE_A4  440
#define NOTE_B4  494
#define NOTE_C5  523
#define NOTE_D5  587
#define NOTE_E5  659
#define NOTE_F5  698
#define NOTE_G5  784
#define NOTE_A5  880
//durée en milliseconde pour chaque note (dans l'ordre)
int type_Rythm[] = {
  500,500,500,500, 2000,0
};

//Note à jouer (dans l'ordre)
int type_Note[] = {
  NOTE_G5, NOTE_A5, NOTE_F5, NOTE_F4, NOTE_C5,0
};

long temps;
long temps_attente ;

int16_t ax, ay, az;  //mesures brutes
int16_t gx, gy, gz;
float accz;
float frequence_hz;

long temps_bip =1000;
long temps_faux_depart;
long temps_reaction;


int broche_HP =9;

bool state;


void setup() {
  // put your setup code here, to run once:
      Wire.begin();  // bus I2C
      Serial.begin(9600); // liaison série
      //startTime = millis(); // Enregistre le temps de début
      while (!Serial) {
        ; // wait for serial port to connect. Needed for native USB (LEONARDO)
      }
      accelgyro.initialize();  // initialize device
       pinMode(8,OUTPUT); //on prépare le pin 46 en mode sortie
      state = true;
      musique_depart();

     
}

void loop() {
  // put your main code here, to run repeatedly:
      
 
    accelgyro.getAcceleration(&ax, &ay, &az);
    accz = az*9.81/16384;
    Serial.println(accz); 
    temps_attente = random(8000,12000);
    
  if  (millis()<temps_attente){

    
    if ( abs(accz) > 15){ 
    // Arrêter le programme
        temps_faux_depart = millis();
        Serial.print("Valeur limite atteinte. Programme arrêté à t =");
        Serial.print("\t");
        Serial.print(temps_faux_depart);
        Serial.print("\t");
        Serial.println("ms");
        Serial.print("Le bip devait partir à  t =");
        Serial.print("\t");
        Serial.print(temps_attente);
        Serial.print("\t");
        Serial.println("ms");

        
        state = false;


          while (state == false) {
         //Boucle infinie pour maintenir l'arrêt du programme
          }
       }    
  else{
    Serial.println(accz);
    
      }
  }
  
   else{
    
   tone(broche_HP,frequence_hz);
          //On attend X millisecondes (durée de la note) avant de passer à la suivante
    delay(temps_bip);
      //On arrête la lecture de la note
     noTone(broche_HP);
     while (state == true){
      accelgyro.getAcceleration(&ax, &ay, &az);
      accz = az*9.81/16384;
      temps = millis();
      Serial.print(temps); 
      Serial.print("\t");
      Serial.println(accz);
      }
   }
    
 }
 
      
   


void musique_depart(){
     int i = 0;
      // Lecture du tableau de note ... lorsque nous lisons un 0  c'est que c'est la fin
  while (type_Note[i] != 0){
      //On joue la note
    tone(broche_HP, type_Note[i]);
          //On attend X millisecondes (durée de la note) avant de passer à la suivante
    delay(type_Rythm[i]);
      //On arrête la lecture de la note
    noTone(broche_HP);
      //On marque une courte pause (entre chaque note, pour les différencer)
    delay(50);
      //On passe à la note suivante
    ++i;
  }
}
