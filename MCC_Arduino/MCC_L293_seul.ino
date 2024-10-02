int Moteur_sens1=4; // Pin 4 Arduino vers broche INPUT1 du L293D
int Moteur_sens2=2; // Pin 5 Arduino vers broche INPUT2 du L293D
int moteur1_PWM = 3; // Pin 10 Arduino PWM vers EN1 du L293D
int PWM=255; // Variable PWM image de la vitesse

void setup() {
  Serial.begin(9600); // Ouverture du port série et debit de communication fixé à 9600 bauds
  pinMode(moteur1_PWM, OUTPUT); // Pin 3 Arduino en sortie PWM
  pinMode(Moteur_sens1, OUTPUT); // Pin 4 Arduino en sortie digitale
  pinMode(Moteur_sens2, OUTPUT); // Pin 5 Arduino en sortie digitale
  delay( 1000 ); // Attendre 1 seconde avant le lancement de la fonction accélération
  
}

void loop() {
  // Le moteur tourne dans le sens normal
  digitalWrite(Moteur_sens1, HIGH); // Activation de la broche INPUT1 du L293D
  digitalWrite(Moteur_sens2, LOW); // Désactivation de la broche INPUT2 du L293D
  analogWrite(moteur1_PWM,PWM); // Envoi du signal PWM sur la sortie analogique 10
  delay( 3000 ); // Attendre 3 secondes
  
  // Le moteur est à l'arrêt
  digitalWrite(Moteur_sens1, LOW); // Désactivation de la broche INPUT1 du L293D
  digitalWrite(Moteur_sens2, LOW); // Désactivation INPUT2 du L293D
  analogWrite(moteur1_PWM,PWM); // Envoi du signal PWM sur la sortie analogique 10
  delay( 3000 ); // Attendre 3 secondes
  
  // Le moteur tourne dans le sens inverse
  digitalWrite(Moteur_sens1, LOW); // Désactivation de la broche INPUT1 du L293D
  digitalWrite(Moteur_sens2, HIGH); // Activation de la broche INPUT2 du L293D
  analogWrite(moteur1_PWM,PWM); // Envoi du signal PWM sur la sortie analogique 10
  delay( 3000 ); // Attendre 3 secondes
  
  // Le moteur est à l'arrêt
  digitalWrite(Moteur_sens1, LOW); // Désactivation de la broche INPUT1 du L293D
  digitalWrite(Moteur_sens2, LOW); // Désactivation de la broche INPUT2 du L293D
  analogWrite(moteur1_PWM,PWM); // Envoi du signal PWM sur la sortie analogique 10
  delay( 3000 ); // Attendre 3 secondes
}
