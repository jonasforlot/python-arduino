 #include <Servo.h>

// -------------------------
// Entrées des capteurs
// -------------------------
const int CAPTEUR_EO = A0;
const int CAPTEUR_NS = A1;

// -------------------------
// Servomoteurs
// -------------------------
const int SERVO_EO = 9;
const int SERVO_NS = 10;

Servo MonServo1;
Servo MonServo2;

// -------------------------
// Position des servomoteurs
// -------------------------
int angleEO = 90;
int angleNS = 90;

// Limites mécaniques
const int ANGLE_MIN = 10;
const int ANGLE_MAX = 170;

// -------------------------
// Réglages des capteurs
// -------------------------

// Valeur correspondant à l'équilibre du pont
const int CENTRE = 512;

// Zone dans laquelle on considère que le capteur est équilibré
const int ZONE_MORTE = 15;

// -------------------------
// Moyenne des mesures
// -------------------------
const int N = 5;


void setup() {

  MonServo1.attach(SERVO_EO);
  MonServo2.attach(SERVO_NS);

  // Position initiale
  MonServo1.write(angleEO);
  MonServo2.write(angleNS);

  Serial.begin(9600);
}


void loop() {

  // -------------------------
  // Lecture moyenne du capteur EO
  // -------------------------

  long sommeEO = 0;
  long sommeNS = 0;

  for (int i = 0; i < N; i++) {

    sommeEO += analogRead(CAPTEUR_EO);
    sommeNS += analogRead(CAPTEUR_NS);

    delay(2);
  }

  int ValEO = sommeEO / N;
  int ValNS = sommeNS / N;


  // -------------------------
  // Axe Est-Ouest
  // -------------------------

  if (ValEO > CENTRE + ZONE_MORTE) {

    if (angleEO < ANGLE_MAX) {
      angleEO++;
    }
  }

  else if (ValEO < CENTRE - ZONE_MORTE) {

    if (angleEO > ANGLE_MIN) {
      angleEO--;
    }
  }


  // -------------------------
  // Axe Nord-Sud
  // -------------------------

  if (ValNS < CENTRE - ZONE_MORTE) {

    if (angleNS < ANGLE_MAX) {
      angleNS++;
    }
  }

  else if (ValNS > CENTRE + ZONE_MORTE) {

    if (angleNS > ANGLE_MIN) {
      angleNS--;
    }
  }


  // -------------------------
  // Commande des servomoteurs
  // -------------------------

  MonServo1.write(angleEO);
  MonServo2.write(angleNS);


  // -------------------------
  // Affichage dans le moniteur série
  // -------------------------

  Serial.print("EO : ");
  Serial.print(ValEO);

  Serial.print("   NS : ");
  Serial.print(ValNS);

  Serial.print("   Angle EO : ");
  Serial.print(angleEO);

  Serial.print("   Angle NS : ");
  Serial.println(angleNS);


  delay(50);
}
