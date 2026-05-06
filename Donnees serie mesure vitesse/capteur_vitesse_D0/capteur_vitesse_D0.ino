
int sensor = 3; // broche pour détection du capteur
int etatSensor ; // état du capteur (haut ou bas)

int delai = 100; // temps de comptage en ms
int nb_trous =20 ; // nombre de trous de la roue codeuse
bool etat_old= false ; // 
bool  etat_new = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
int compt=0; // comptage initialisé à 0
float rps=0; // vitesse intialisée à 0
long temps; //mesure du temps pour l'acquisition

void setup() 
{
  
  pinMode(sensor,INPUT); // la broche A0 est déclarée comme entrée
  Serial.begin(115200); // pour le moniteur série
  temps = millis(); // mesure du temps 
}  
 
void loop()
{
  Calcul_Vitesse();

}

// Programme de calcul de la vitesse
void Calcul_Vitesse() {
  etat_new = digitalRead(sensor);
 

 // Boucle de comptage des chagements d'état
  if (etat_old != etat_new) {
    etat_old = etat_new;
    compt = compt + 1;
  }


  // Boucle de calcul de la vitesse mesurée
  if (millis() > (temps + delai)) {
    rps = float(compt) / delai * 1000 / (2*nb_trous) ; // il faut diviser par 2 car pour chaque trou , deux changements d'état vont être détectés
    Serial.print("temps  ");
    Serial.print(temps);
    Serial.print("  rps ");
    Serial.println(rps);
    temps = millis();
    compt = 0;
  }
}
