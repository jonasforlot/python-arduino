int sensor = A0; // broche pour détection du capteur
const int motorPin = 9; // broche pour contrôler le rapport cyclique (vitesse du moteur)
unsigned long start_time = 0; // temps de début d'un comptage
unsigned long end_time = 0; // temps de fin d'un comptage
int compt = 0; // comptage initialisé à 0
float rps = 0; // vitesse initialisée à 0
unsigned long temps_detection = 0; // mesure du temps pour la détection par le capteur
bool verif_4ms = false; // indicateur pour le délai de 4 ms
unsigned long temps_verif_start = 0; // moment de début de la vérification de 4 ms

void setup() {
  pinMode(motorPin, OUTPUT);
  analogWrite(motorPin, 160); // vitesse de rotation entre 0 et 255 (0 à 100%)
  Serial.begin(9600);
}

void loop() {
  compt = 0;
  start_time = millis(); // début de la mesure du temps
  end_time = start_time + 1000; // comptage sur 1 seconde

  while (millis() < end_time) { // comptage sur une seconde
    int valeur = analogRead(sensor); // lire la valeur du capteur

    if (valeur > 50 && !verif_4ms) { // Détection d'une salve
      compt++; // incrémentation du compteur
      verif_4ms = true; // début de la vérification des 4 ms
      temps_verif_start = millis(); // enregistre le début de la vérification
    }

    // Si on est en train de vérifier le signal pendant 4 ms
    if (verif_4ms) {
      if (millis() - temps_verif_start >= 4) { // vérifie si 4 ms sont écoulées
        verif_4ms = false; // Fin de la vérification
      } else {
        // Pendant les 4 ms, si le signal dépasse à nouveau 50, on recommence le délai de 4 ms
        if (valeur > 50) {
          temps_verif_start = millis(); // réinitialisation du début de la vérification
        }
      }
    }
  }

  // Calculer les rotations par seconde (ou changements d'état par seconde)
  rps = float(compt/2); // 2 impulsions à chaque tour

  Serial.print(millis());
  Serial.print("\t");
  Serial.println(rps);
}
