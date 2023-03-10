const int enPin=8;

const int stepPin = 3; //Y.STEP
const int dirPin = 6; // Y.DIR

const int stepsPerRev=200;
int pulseWidthMicros = 100;   // microseconds
int millisBtwnSteps = 50;
void setup() {
  Serial.begin(9600);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  Serial.println(F("CNC Shield Initialized"));
}
void loop() {
  Serial.println(F("Running clockwise"));
  digitalWrite(dirPin, HIGH); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for (int i = 0; i < 8*stepsPerRev; i++) {
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(pulseWidthMicros);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(millisBtwnSteps);
  }

  
}
