//Parameters

const int directionA  = 12;
const int directionB  = 13;
const int rateA  = 3;
const int rateB  = 11;
float freq = 3; entre 3 et 6 Hz, // adapter la tension d'alimentation selon la vitesse
int microsBtwnSteps ;
int vitesse=255 ;

void setup() {
  //Init Serial USB
  Serial.begin(9600);
  Serial.println(F("Initialize System"));
  microsBtwnSteps = int(5000/freq);
  //Init Motor Shield
  pinMode(directionA, OUTPUT); //Initiates Motor Channel A pin
  pinMode(directionB, OUTPUT); //Initiates Motor Channel B pin
}

void loop() {
  
  testStepperMS();
}

void testStepperMS() { /* function testStepperMS */
  //// Test stepper
  Serial.println("Move stepper 10 step clockwise");
  stpCW(50);
//  delay(1000);
//  Serial.println("Move stepper 2 step counter clockwise");
//  stpCCW(100);
//  delay(1000);
}


void stpCW(int nbstep) { /* function stpCW */
  //// Move stepper clockwise
  for (int i = 0; i < nbstep; i++) {
    
    digitalWrite(directionA, HIGH);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB
    , 0);   
    delayMicroseconds(microsBtwnSteps);

    
    digitalWrite(directionB, LOW);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(microsBtwnSteps);

    
    digitalWrite(directionA, LOW);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(microsBtwnSteps);

   
    digitalWrite(directionB, HIGH);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(microsBtwnSteps);
  }
}

void stpCCW(int nbstep) { /* function stpCCW */
  //// Move stepper counter-clockwise
  for (int i = 0; i < nbstep; i++) {
    
    digitalWrite(directionA, HIGH);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(microsBtwnSteps);

   
    digitalWrite(directionB, HIGH);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(microsBtwnSteps);

    
    digitalWrite(directionA, LOW);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(microsBtwnSteps);

    
    digitalWrite(directionB, LOW);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(microsBtwnSteps);
  }
}
