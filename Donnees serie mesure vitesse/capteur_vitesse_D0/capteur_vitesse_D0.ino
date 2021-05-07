
int sensor = 3; // broche pour détection du capteur
int etatSensor ; // état du capteur (haut ou bas)
unsigned long start_time=0; //temps de début d'un comptage
unsigned long end_time =0; //temps de fin d'un comptage
 
int nb_trous =20 ; // nombre de trous de la roue codeuse
int etat_old= 1 ; // 
int  etat_new = 1; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
int compt=0; // comptage initialisé à 0
float rps=0; // vitesse intialisée à 0
long temps; //mesure du temps pour l'acquisition

void setup() 
{
  
  pinMode(sensor,INPUT); // la broche 3 est déclarée comme entrée
  Serial.begin(9600); // pour le moniteur série
  temps = millis(); // mesure du temps 
}  
 
void loop()
{
 compt = 0;
 start_time=millis(); //on mesure le temps
 end_time=start_time+1000; // pour un comptage toutes les secondes
 temps = millis(); //mesure du temps pour l'acquisition
 

while(millis()<end_time){ // comptage sur une seconde
  etat_new = digitalRead(sensor);
  if (etat_old  != etat_new) { // petite boucle pour incrémenter le compteur à chaque changement d'état lu par le capteur
    etat_old = etat_new;
    compt = compt+1;
  }  
}

rps = float(compt)/(2*nb_trous) ; // il faut diviser par 2 car pour chaque trou , deux changements d'état vont être détectés

Serial.print("temps  ");
Serial.print(temps);
Serial.print("  rps ");
Serial.println(rps);


   
}
