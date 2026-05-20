#define borneENA        6      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        5       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        10       // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        9       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        8       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        11       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
//*****************************************mesure vitesse************************************************
int K=1 ;
float PWMmot1 ;
float PWMmot2 ;
float PWMmot1arr ;
float PWMmot2arr ;
int sensor1 = A0; // broche pour détection du capteur
int etatSensor1 ; // état du capteur (haut ou bas)
unsigned long start_time=0; //temps de début d'un comptage
unsigned long end_time =0; //temps de fin d'un comptage
long temps;
int nb_trous =20 ; // nombre de trous de la roue codeuse
int delai = 500; // temps de comptage en ms
bool etat_old1= false ; // 
bool  etat_new1 = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)
int compt1=0; // comptage initialisé à 0
float rps1=0; // vitesse intialisée à 0
int compt2=0; // comptage initialisé à 0
float rps2=0; // vitesse intialisée à 0
//2
int sensor2 = A1;
int etatSensor2 ;
bool etat_old2= false ; // 
bool  etat_new2 = false; // les états vont changer à chaque chaque modiication de la valeu lue par le capteur (haut/5V ou bas/0V)

void moteurarriere1(){
    digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
    digitalWrite(borneIN2, LOW);                  // L'entrée IN2 doit être au niveau bas
  


  // Et on lance les moteurs 
  analogWrite(borneENA, PWMmot1arr);       // Active l'alimentation du moteur 1
  
}

//2
void moteurarriere2(){

  
  // Moteur B
  digitalWrite(borneIN3, HIGH);                 // L'entrée IN3 doit être au niveau haut
  digitalWrite(borneIN4, LOW);                  // L'entrée IN4 doit être au niveau bas

  // Et on lance les moteurs 

  analogWrite(borneENB, PWMmot2arr);       // Active l'alimentation du moteur 2
}

void moteuravant1(){
// Moteur A
  digitalWrite(borneIN1, LOW);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, HIGH);                // L'entrée IN2 doit être au niveau bas
  

  // Et on lance les moteurs 
  analogWrite(borneENA, PWMmot1);       // Active l'alimentation du moteur 1
 
}


void moteuravant2(){

  // Moteur B
  digitalWrite(borneIN3, LOW);                 // L'entrée IN3 doit être au niveau haut
  digitalWrite(borneIN4, HIGH);                // L'entrée IN4 doit être au niveau bas

  // Et on lance les moteurs 
   analogWrite(borneENB, PWMmot2);       // Active l'alimentation du moteur 1

}
void setup(){
  Serial.begin(9600); // pour le moniteur série
  temps = millis(); // mesure du temps
//2
  pinMode(borneENA, OUTPUT);
  pinMode(borneIN1, OUTPUT);
  pinMode(borneIN2, OUTPUT);
  pinMode(borneIN3, OUTPUT);
  pinMode(borneIN4, OUTPUT);
  pinMode(borneENB, OUTPUT);
}
void loop() {
  PWMmot1=200;
  PWMmot2=200;
   moteuravant1();
   moteuravant2();
  //moteurarriere1();
  //moteurarriere2();
  Calcul_Vitesse();


 
}

// Programme de calcul de la vitesse 1
void Calcul_Vitesse() {
  if (analogRead(sensor1)< 50){
    etat_new1 = true; 
  }
  else {
    etat_new1 =false;
  }

 // Boucle de comptage des chagements d'état
  if (etat_old1 != etat_new1) {
    etat_old1 = etat_new1;
    compt1 = compt1 + 1;
  }

  if (analogRead(sensor2)< 30){
    etat_new2 = true; 
  }
  else {
    etat_new2 =false;
  }

 // Boucle de comptage des chagements d'état
  if (etat_old2 != etat_new2) {
    etat_old2 = etat_new2;
    compt2 = compt2 + 1;
  }



  // Boucle de calcul de la vitesse mesurée
  if (millis() > (temps + delai)) {
    rps1 = float(compt1) / delai * 1000 / (2*nb_trous) ; // il faut diviser par 2 car pour chaque trou , deux changements d'état vont être détectés
    rps2 = float(compt2) / delai * 1000 / (2*nb_trous) ; // il faut diviser par 2 car pour chaque trou , deux changements d'état vont être détectés
    Serial.print("temps  ");
    Serial.print(temps);
    Serial.print("  rps1 ");
    Serial.print(rps1);
    Serial.print("  rps2 ");
    Serial.println(rps2);
    temps = millis();
    compt1 = 0;
    compt2 = 0;
  }
}
