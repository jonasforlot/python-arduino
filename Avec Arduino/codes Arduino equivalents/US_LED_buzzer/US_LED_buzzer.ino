/* 
 * Code d'exemple pour un capteur à ultrasons HC-SR04.
 */

/* Constantes pour les broches */
const byte TRIGGER_PIN = 13; // Broche TRIGGER
const byte ECHO_PIN = 12;    // Broche ECHO
const byte LED_verte = 8; // broches pour les LED et le buzzer
const byte LED_orange = 9;
const byte LED_rouge = 10;
const byte buzzer = 11;



 
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
  pinMode (LED_verte, OUTPUT); // On déclare les broches des LED et buzzer comme sorties
  pinMode (LED_orange, OUTPUT);
  pinMode (LED_rouge, OUTPUT);
  pinMode (buzzer, OUTPUT);
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
  
 // zone pour laquelle la LED verte clignote , buzzer à 440 Hz
if ((distance_mm < 500.0)and (distance_mm > 300.0)) {
digitalWrite (LED_verte, HIGH); //la LED s'allume pendant 1 s et s'éteint pendant 0,5 s
tone (buzzer,440);  //buzzer à 440 Hz
delay(1000);
digitalWrite (LED_verte,LOW);
noTone (buzzer);
delay (500);
 }
 
//zone pour laquelle la LED orange clignote , buzzer à 880 Hz
if ((distance_mm < 300.0) and (distance_mm > 100.0)) { //la LED s'allume pendant 0,5 s et s'éteint pendant 0,25 s
digitalWrite (LED_orange, HIGH); 
tone (buzzer,880); //buzzer à 880 Hz
delay(500);
digitalWrite (LED_orange,LOW);
noTone (buzzer);
delay (250);
}

//zone pour laquelle la LED rouge clignote , buzzer à 1760 Hz
 if (distance_mm < 100.0) { //la LED s'allume pendant 0,1 s et s'éteint pendant 0,05 s
digitalWrite (LED_rouge, HIGH); 
tone (buzzer,1760);// buzzer à 1760 Hz
delay(100);
digitalWrite (LED_rouge,LOW);
noTone (buzzer);
delay (50);

 }

// sinon il ne se passe rien ... 
else {
  digitalWrite (LED_verte,LOW);
  digitalWrite (LED_orange,LOW);
  digitalWrite (LED_rouge,LOW);
  delay (50);
  
}
    
  
  /* Affiche les résultats en mm*/

  Serial.print("distance en mm : ");
  Serial.print(distance_mm);
  Serial.println(" mm, ");

//   
  /* Délai d'attente pour éviter d'afficher trop de résultats à la seconde */
  delay(500);
}
