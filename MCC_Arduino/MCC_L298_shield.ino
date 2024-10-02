
int PWM=255; // Variable PWM image de la vitesse

int directionPin = 12; // broche pour le sens de rotation du moteur
int pwmPin = 3; // broche PWM pour contrôler la vitesse 
int brakePin = 9; // broche pour activer/désactiver le frein

//décommnenter pour utiliser le canal B
//int directionPin = 13;
//int pwmPin = 11;
//int brakePin = 8;



void setup() {
  
// définition des broches
pinMode(directionPin, OUTPUT);
pinMode(pwmPin, OUTPUT);
pinMode(brakePin, OUTPUT);

}

void loop() {


// Le moteur tourne dans le sens horaire
digitalWrite(directionPin, HIGH);// indique le sens de rotation
digitalWrite(brakePin, LOW);// relâche le frein
analogWrite(pwmPin, PWM);// indique la vitesse de rotation
delay(3000); // Attendre 3 secondes

//Arrêt du moteur
digitalWrite(brakePin, HIGH);// active le frein
analogWrite(pwmPin, 0);// on remet la valeur de vitesse de rotation à 0
delay(3000); // Attendre 3 secondes

// Le moteur tourne dans le sens anti horaire
digitalWrite(directionPin, LOW);// indique le sens de rotation
digitalWrite(brakePin, LOW);// relâche le frein
analogWrite(pwmPin, PWM);// indique la vitesse de rotation
delay(3000); // Attendre 3 secondes

//Arrêt du moteur
digitalWrite(brakePin, HIGH);// active le frein
analogWrite(pwmPin, 0);// on remet la valeur de vitesse de rotation à 0
delay(3000); // Attendre 3 secondes


}
