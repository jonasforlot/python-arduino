
//*******************************************************************************//
// Association des entrées du L298N, aux sorties utilisées sur notre Arduino Uno //
//*******************************************************************************//
#define borneENA        23      // On associe la borne "ENA" du L298N à la pin D10 de l'arduino
#define borneIN1        22       // On associe la borne "IN1" du L298N à la pin D9 de l'arduino
#define borneIN2        21      // On associe la borne "IN2" du L298N à la pin D8 de l'arduino
#define borneIN3        19       // On associe la borne "IN3" du L298N à la pin D7 de l'arduino
#define borneIN4        18       // On associe la borne "IN4" du L298N à la pin D6 de l'arduino
#define borneENB        5       // On associe la borne "ENB" du L298N à la pin D5 de l'arduino
int PWM=128; // Variable PWM image de la vitesse

//*******//
// SETUP //
//*******//
void setup() {
  
  // Configuration de toutes les pins de l'Arduino en "sortie" (car elles attaquent les entrées du module L298N)
  pinMode(borneENA, OUTPUT);
  pinMode(borneIN1, OUTPUT);
  pinMode(borneIN2, OUTPUT);
  pinMode(borneIN3, OUTPUT);
  pinMode(borneIN4, OUTPUT);
  pinMode(borneENB, OUTPUT);
}

//**************************//
// Boucle principale : LOOP //
//**************************//
void loop() {

  // Configuration du L298N en "marche avant", pour les 2 moteurs connectés au pont A et au pont B. Selon sa table de vérité, il faut que :
  // Moteur A
  digitalWrite(borneIN1, HIGH);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, LOW);                  // L'entrée IN2 doit être au niveau bas
  
  // Moteur B
  digitalWrite(borneIN3, HIGH);                 // L'entrée IN3 doit être au niveau haut
  digitalWrite(borneIN4, LOW);                  // L'entrée IN4 doit être au niveau bas

  // Et on lance les moteurs 
  analogWrite(borneENA, PWM);       // Active l'alimentation du moteur 1
  analogWrite(borneENB, PWM);       // Active l'alimentation du moteur 2

  delay(1000);                        // et attend 3 secondes

  // Arrêt des moteurs pendant 3 secondes
 
  digitalWrite(borneIN1, LOW);
  digitalWrite(borneIN2, LOW);
  
  digitalWrite(borneIN3, LOW);
  digitalWrite(borneIN4, LOW);
  
  analogWrite(borneENB, 0);
  analogWrite(borneENA, 0);
  delay(1000);    
  
  // Puis on configure le L298N en "marche arrière",  pour les 2 moteurs connectés au pont A et au pont B. Selon sa table de vérité, il faut que :
  // Moteur A
  digitalWrite(borneIN1, LOW);                 // L'entrée IN1 doit être au niveau haut
  digitalWrite(borneIN2, HIGH);                // L'entrée IN2 doit être au niveau bas
  
  // Moteur B
  digitalWrite(borneIN3, LOW);                 // L'entrée IN3 doit être au niveau haut
  digitalWrite(borneIN4, HIGH);                // L'entrée IN4 doit être au niveau bas

  // Et on lance les moteurs 
  analogWrite(borneENA, PWM);       // Active l'alimentation du moteur 1
  analogWrite(borneENB, PWM);       // Active l'alimentation du moteur 2

  delay(1000);                        // et attend 3 secondes

//  // Arrêt des moteurs pendant 3 secondes
 
  digitalWrite(borneIN1, LOW);
  digitalWrite(borneIN2, LOW);
  
  digitalWrite(borneIN3, LOW);
  digitalWrite(borneIN4, LOW);
  
  analogWrite(borneENB, 0);
  analogWrite(borneENA, 0);
  delay(1000);  
}
