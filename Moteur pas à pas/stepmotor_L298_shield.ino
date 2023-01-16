//Parameters

const int directionA  = 12;
const int directionB  = 13;
const int rateA  = 3;
const int rateB  = 11;
int millisBtwnSteps = 2000;
int vitesse=255 ;

void setup() {
  //Init Serial USB
  Serial.begin(9600);
  Serial.println(F("Initialize System"));
  //Init Motor Shield
  pinMode(directionA, OUTPUT); //Initiates Motor Channel A pin
  pinMode(directionB, OUTPUT); //Initiates Motor Channel B pin
}

void loop() {
  
  testStepperMS();
}

void testStepperMS() { /* function testStepperMS */
  //// Test stepper
  Serial.println("Move stepper 1 step clockwise");
  stpCW(50);
  delay(1000);
  Serial.println("Move stepper 2 step counter clockwise");
  stpCCW(100);
  delay(1000);
}


void stpCW(int nbstep) { /* function stpCW */
  //// Move stepper clockwise
  for (int i = 0; i < nbstep; i++) {
    
    digitalWrite(directionA, HIGH);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB
    , 0);   
    delayMicroseconds(millisBtwnSteps);

    
    digitalWrite(directionB, LOW);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(millisBtwnSteps);

    
    digitalWrite(directionA, LOW);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(millisBtwnSteps);

   
    digitalWrite(directionB, HIGH);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(millisBtwnSteps);
  }
}

void stpCCW(int nbstep) { /* function stpCCW */
  //// Move stepper counter-clockwise
  for (int i = 0; i < nbstep; i++) {
    
    digitalWrite(directionA, HIGH);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(millisBtwnSteps);

   
    digitalWrite(directionB, HIGH);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(millisBtwnSteps);

    
    digitalWrite(directionA, LOW);   //Set direction of CH A
    analogWrite(rateA, 255);   
    analogWrite(rateB, 0);   
    delayMicroseconds(millisBtwnSteps);

    
    digitalWrite(directionB, LOW);   //Set direction of CH B
    analogWrite(rateB, 255);   
    analogWrite(rateA, 0);   
    delayMicroseconds(millisBtwnSteps);
  }
}
