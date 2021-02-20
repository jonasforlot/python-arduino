/* 
 * Code d'exemple pour un capteur à ultrasons HC-SR04.
 */

/* Constantes pour les broches */
const byte TRIGGER_PIN = 13; // Broche TRIGGER
const byte ECHO_PIN = 12;    // Broche ECHO
const byte LED_verte = 8; // broches pour les LED 
const byte LED_orange = 9;
const byte LED_rouge = 10;



 
/* Constantes pour le timeout */
const unsigned long MEASURE_TIMEOUT = 25000UL; // 25ms = ~8m à 340m/s, temps limite pour la mesure de distance

/* Vitesse du son dans l'air en mm/us */
const float SOUND_SPEED = 340.0 / 1000;

/** Fonction setup() */
void setup() {
   
  /* Initialise le port série */
  Serial.begin(9600);
   
  /* Initialise les broches */
  pinMode(TRIGGER_PIN, OUTPUT);
  digitalWrite(TRIGGER_PIN, LOW); // La broche TRIGGER doit être à LOW au repos
  pinMode(ECHO_PIN, INPUT);

//  
}
 
/** Fonction loop() */
void loop() {
  
  /* 1. Lance une mesure de distance en envoyant une impulsion HIGH de 10µs sur la broche TRIGGER */
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);
  
  /* 2. Mesure le temps en us entre l'envoi de l'impulsion ultrasonique et son écho (si il existe) */
  long measure = pulseIn(ECHO_PIN, HIGH, MEASURE_TIMEOUT);
   
  /* 3. Calcul de la distance à partir du temps mesuré */
  float distance_mm = measure / 2.0 * SOUND_SPEED;
  

  
  /* Affiche les résultats en mm */

  Serial.print("distance en mm : ");
  Serial.print(distance_mm);
  Serial.println(" mm, ");

//   
  /* Délai d'attente pour éviter d'afficher trop de résultats à la seconde */
  delay(500);
}
