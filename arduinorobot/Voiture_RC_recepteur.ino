#include <SoftwareSerial.h>

// Moteur 1
int ENA = 5; // Broche de signal pour la vitesse du moteur 1
int IN1 = 6; // Broche de commande 1 du moteur 1
int IN2 = 7; // Broche de commande 2 du moteur 1

// Moteur 2
int ENB = 10; // Broche de signal pour la vitesse du moteur 2
int IN3 = 11; // Broche de commande 1 du moteur 2
int IN4 = 12; // Broche de commande 2 du moteur 2

SoftwareSerial BTSerial(2, 3); // RX, TX pour le module HC-05

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.begin(9600); // Initialisation de la communication série avec le moniteur série
  BTSerial.begin(9600); // Initialisation de la communication série avec le module HC-05
}

void loop() {
  if (BTSerial.available()) {
    String data = BTSerial.readStringUntil('\n');

    // Décoder les données reçues
    int separatorIndex = data.indexOf("\t");
    if (separatorIndex != -1) {
      String x_val_str = data.substring(0, separatorIndex);
      String y_val_str = data.substring(separatorIndex + 1);

      // Convertir les valeurs en entiers
      int x_val = x_val_str.toInt();
      int y_val = y_val_str.toInt();

      // Affichage des valeurs des axes X et Y dans le moniteur série
//      
      Serial.print(x_val);
      Serial.print("\t");
      Serial.println(y_val);

      // Contrôler les moteurs en fonction des valeurs des axes
      controlMotors(x_val, y_val);
      delay(100);
    }
    
  }
//  else{
//    Serial.println("pas de signal");
//  }
}

void controlMotors(int x_val, int y_val) {
  // Convertir les valeurs de l'axe Y en vitesses des moteurs
  int motor_speed_y = map(y_val, 0, 1023, -255, 255);

  // Définir une vitesse fixe pour la rotation
  int rotation_speed = 100;

  // Contrôler la direction des moteurs en fonction de l'axe X du joystick
  if (x_val < 450) { // Joystick penché à gauche
    // Tourner à gauche sur place
    analogWrite(ENA, rotation_speed);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENB, rotation_speed);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else if (x_val > 550) { // Joystick penché à droite
    // Tourner à droite sur place
    analogWrite(ENA, rotation_speed);
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    analogWrite(ENB, rotation_speed);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
  } else { // Joystick centré ou en position intermédiaire
    // Avancer ou reculer
    if (motor_speed_y > 0) {
      // Avancer
      analogWrite(ENA, abs(motor_speed_y/2));
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENB, abs(motor_speed_y/2));
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    } else if (motor_speed_y < 0) {
      // Reculer
      analogWrite(ENA, abs(motor_speed_y/2));
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      analogWrite(ENB, abs(motor_speed_y/2));
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
    } else {
      // Arrêter
      analogWrite(ENA, 0);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      analogWrite(ENB, 0);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
    }
  }
}
