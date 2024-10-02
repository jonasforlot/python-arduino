
const int motorPin =  9; // Numéro de broche pour contrôler le rapport cyclique, et donc la vitesse de rotation du moteur


void setup() {
  // On définit la broche du moteur comme une sortie :
  pinMode(motorPin, OUTPUT);

}

void loop() {

  // vitesse de rotation à 50 % (avec l'instruction analogWrite)
    analogWrite(motorPin, 128);
  
 
}
