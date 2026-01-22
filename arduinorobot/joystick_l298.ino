// Moteur 1
int ENA = 5; // Broche de signal pour la vitesse du moteur 1
int IN1 = 6; // Broche de commande 1 du moteur 1
int IN2 = 7; // Broche de commande 2 du moteur 1

// Moteur 2
int ENB = 10; // Broche de signal pour la vitesse du moteur 2
int IN3 = 11; // Broche de commande 1 du moteur 2
int IN4 = 12; // Broche de commande 2 du moteur 2

// Broches pour le joystick GT1079
int joystick_x_pin = A0;
int joystick_y_pin = A1;

void setup() {
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  
  Serial.begin(9600); // Initialisation de la communication série
}

void loop() {
  int x_val = analogRead(joystick_x_pin); // Lire la valeur de l'axe X du joystick
  int y_val = analogRead(joystick_y_pin); // Lire la valeur de l'axe Y du joystick

  // Affichage des valeurs des axes X et Y dans le moniteur série
  Serial.print("X : ");
  Serial.print(x_val);
  Serial.print("\tY : ");
  Serial.println(y_val);

  // Convertir les valeurs analogiques en vitesses des moteurs
  int motor_speed_y = map(y_val, 0, 1023, -255, 255);

  // Définir une vitesse fixe pour la rotation
  int rotation_speed = 200;

  // Contrôler la direction des moteurs en fonction de l'axe X du joystick
  if (x_val < 400) { // Joystick penché à gauche
    // Tourner à gauche sur place
    analogWrite(ENA, rotation_speed);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    analogWrite(ENB, rotation_speed);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
  } else if (x_val > 600) { // Joystick penché à droite
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
      analogWrite(ENA, abs(motor_speed_y));
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      analogWrite(ENB, abs(motor_speed_y));
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
    } else if (motor_speed_y < 0) {
      // Reculer
      analogWrite(ENA, abs(motor_speed_y));
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      analogWrite(ENB, abs(motor_speed_y));
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

  delay(100); // Délai pour éviter une lecture trop rapide du joystick
}
